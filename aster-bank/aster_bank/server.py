"""Serve the Aster Bank browser app and its local, SQLite-backed banking API."""

from contextlib import closing, contextmanager
from datetime import datetime, timezone
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import secrets
import sqlite3
import sys
from urllib.parse import urlsplit

from .bank import Bank, BankError, seed_bank
from .package import build_source_zip, documentation_path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = ROOT / ".data" / "bank.sqlite"

_TENANT = "local-sandbox"
_DEMO_USER = "customer-ayesha"
_SESSION_COOKIE = "aster_session"
_VISIT_COOKIE = "aster_visited"
_SESSION_SECONDS = 8 * 60 * 60
_VISIT_SECONDS = 365 * 24 * 60 * 60
_MAX_BODY_BYTES = 8192

_API_METHODS = {
    "/api/dashboard": "GET",
    "/api/bootstrap": "POST",
    "/api/login": "POST",
    "/api/register": "POST",
    "/api/logout": "POST",
    "/api/action": "POST",
}

_ASSETS = {
    "/": ("dist/client/index.html", "text/html; charset=utf-8"),
    "/index.html": ("dist/client/index.html", "text/html; charset=utf-8"),
    "/styles.css": ("dist/client/styles.css", "text/css; charset=utf-8"),
    "/app.mjs": ("dist/client/app.mjs", "text/javascript; charset=utf-8"),
    "/aster.svg": ("dist/client/aster.svg", "image/svg+xml"),
    "/inter.woff2": ("dist/client/inter.woff2", "font/woff2"),
    "/docs/use-case.svg": ("docs/use-case.svg", "image/svg+xml"),
    "/docs/transfer-sequence.svg": ("docs/transfer-sequence.svg", "image/svg+xml"),
    "/docs/project-guide.md": ("docs/project-guide.md", "text/plain; charset=utf-8"),
    "/downloads/aster-bank.zip": (None, "application/zip"),
}
_PYTHON_DOCS = {"docs/project-guide.md", "docs/transfer-sequence.svg"}


class ApiError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status = status
        self.code = code


def _unauthenticated():
    return ApiError(401, "UNAUTHENTICATED", "Sign in to continue.")


@contextmanager
def _connection(db_path, *, write=False):
    with closing(sqlite3.connect(db_path, timeout=5)) as connection, connection:
        if write:
            # Reserve the writer before reading the state, across threads and processes.
            connection.execute("BEGIN IMMEDIATE")
        yield connection


def _execute_migration(connection, source):
    # executescript() would implicitly commit the migration transaction.
    start = 0
    for end, character in enumerate(source, 1):
        if character == ";" and sqlite3.complete_statement(source[start:end]):
            connection.execute(source[start:end])
            start = end
    if source[start:].strip():
        connection.execute(source[start:])


def _prepare_database(db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with _connection(db_path) as connection:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("CREATE TABLE IF NOT EXISTS local_migrations (name TEXT PRIMARY KEY NOT NULL)")
    for migration in sorted((ROOT / "drizzle").glob("*.sql")):
        with _connection(db_path, write=True) as connection:
            applied = connection.execute("SELECT 1 FROM local_migrations WHERE name = ?", (migration.name,)).fetchone()
            if not applied:
                _execute_migration(connection, migration.read_text(encoding="utf-8"))
                connection.execute("INSERT INTO local_migrations (name) VALUES (?)", (migration.name,))


def _load_workspace(connection):
    row = connection.execute("SELECT contents FROM banking_workspaces WHERE tenant = ?", (_TENANT,)).fetchone()
    return json.loads(row[0]) if row else None


def _save_workspace(connection, workspace):
    connection.execute(
        """INSERT INTO banking_workspaces (tenant, version, contents) VALUES (?, 1, ?)
           ON CONFLICT (tenant) DO UPDATE SET version = version + 1, contents = excluded.contents""",
        (_TENANT, json.dumps(workspace, ensure_ascii=True, separators=(",", ":"))),
    )


def _cookies(header):
    result = {}
    for entry in header.split(";"):
        name, delimiter, value = entry.partition("=")
        if delimiter:
            result.setdefault(name.strip(), value.strip())
    return result


def _cookie(name, value, max_age):
    return f"{name}={value}; Path=/; HttpOnly; SameSite=Strict; Max-Age={max_age}"


def _token_digest(token):
    return sha256(token.encode("ascii")).hexdigest() if re.fullmatch(r"[0-9a-f]{64}", token) else None


def _timestamp_ms(now):
    return int(now.timestamp() * 1000)


def _session_user(workspace, digest, now):
    session = workspace["sessions"].get(digest) if workspace and digest else None
    return session["userId"] if session and session["expiresAt"] > _timestamp_ms(now) else None


def _require_session(workspace, digest, now):
    user_id = _session_user(workspace, digest, now)
    if not user_id:
        raise _unauthenticated()
    return user_id


def _reject_constant(_value):
    raise ValueError("Invalid JSON number")


class BankServer(ThreadingHTTPServer):
    def __init__(self, address, db_path):
        self.db_path = db_path
        super().__init__(address, _Handler)


class _Handler(BaseHTTPRequestHandler):
    server_version = "AsterBank"
    sys_version = ""
    timeout = 15

    def log_message(self, *_args):
        # Requests never need to print URL queries or authorization details.
        pass

    def _dispatch(self):
        try:
            route = urlsplit(self.path).path
        except ValueError:
            self._reply(400, b"Invalid request path.")
            return
        is_api = route.startswith("/api/")
        try:
            if is_api:
                self._api(route)
            else:
                self._asset(route)
        except (ApiError, BankError) as error:
            self._json({"error": str(error), "code": error.code}, status=error.status)
        except (ConnectionError, TimeoutError):
            self.close_connection = True
        except Exception as error:
            print(f"[Aster server] {type(error).__name__}", file=sys.stderr, flush=True)
            if is_api:
                self._json({"error": "The banking service is temporarily unavailable.", "code": "SERVICE_UNAVAILABLE"}, status=503)
            else:
                self._reply(500, b"Could not complete the request.")

    do_GET = do_HEAD = do_POST = do_OPTIONS = do_PUT = do_PATCH = do_DELETE = _dispatch

    def _reply(self, status, body, content_type="text/plain; charset=utf-8", headers=()):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        for name, value in headers:
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, payload, *, status=200, cookies=()):
        body = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
        headers = [("Cache-Control", "no-store"), *(("Set-Cookie", cookie) for cookie in cookies)]
        self._reply(status, body, "application/json; charset=utf-8", headers)

    def _asset(self, route):
        if route not in _ASSETS:
            self._reply(404, b"Page not found.")
            return
        if self.command not in {"GET", "HEAD"}:
            self._reply(405, b"Method not allowed.", headers=[("Allow", "GET, HEAD")])
            return

        file, content_type = _ASSETS[route]
        policy = "default-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; img-src 'self' data:"
        if route.startswith("/docs/") and content_type == "image/svg+xml":
            policy += "; style-src 'unsafe-inline'"
        headers = [
            ("Referrer-Policy", "same-origin"),
            ("Cache-Control", "no-cache"),
            ("Content-Security-Policy", policy),
        ]
        if file is None:
            body = build_source_zip(ROOT)
            headers.append(("Content-Disposition", 'attachment; filename="aster-bank.zip"'))
        else:
            path = documentation_path(ROOT, file) if file in _PYTHON_DOCS else ROOT / file
            try:
                body = path.read_bytes()
            except FileNotFoundError:
                self._reply(404, b"Page not found.")
                return
        self._reply(200, body, content_type, headers)

    def _check_origin(self):
        origin = self.headers.get("Origin")
        denied = ApiError(403, "ORIGIN_NOT_ALLOWED", "This request must come from Aster Bank.")
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            raise denied
        if origin:
            scheme = "https" if self.headers.get("X-Forwarded-Proto") == "https" else "http"
            host = self.headers.get("Host") or f"localhost:{self.server.server_port}"
            try:
                target = urlsplit(f"{scheme}://{host}")
                hostname, port = target.hostname, target.port
            except ValueError:
                raise denied from None
            if not hostname or target.username or target.path or target.query or target.fragment:
                raise denied
            authority = f"[{hostname}]" if ":" in hostname else hostname
            if port is not None and port != (443 if scheme == "https" else 80):
                authority += f":{port}"
            if origin != f"{scheme}://{authority}":
                raise denied

    def _read_body(self):
        lengths = self.headers.get_all("Content-Length", [])
        encodings = self.headers.get_all("Transfer-Encoding", [])
        invalid = ApiError(400, "INVALID_JSON", "The request contains invalid JSON.")
        too_large = ApiError(413, "REQUEST_TOO_LARGE", "The request is too large.")
        if len(lengths) > 1 or (encodings and (lengths or [encoding.lower() for encoding in encodings] != ["chunked"])):
            raise invalid
        length = lengths[0] if lengths else "0"
        if not re.fullmatch(r"[0-9]+", length):
            raise invalid
        length = length.lstrip("0") or "0"
        if not encodings and length == "0":
            return {}
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            raise ApiError(415, "INVALID_CONTENT_TYPE", "Send a JSON request.")
        if len(length) > len(str(_MAX_BODY_BYTES)) or int(length) > _MAX_BODY_BYTES:
            raise too_large

        raw = self._read_chunked(invalid, too_large) if encodings else self.rfile.read(int(length))
        if not encodings and len(raw) != int(length):
            raise invalid
        try:
            payload = json.loads(raw.decode("utf-8-sig", errors="replace"), parse_constant=_reject_constant) if raw else {}
        except (ValueError, RecursionError):
            raise invalid from None
        if not isinstance(payload, dict):
            raise ApiError(400, "INVALID_JSON", "Send a JSON object.")
        return payload

    def _read_chunked(self, invalid, too_large):
        body = bytearray()
        while True:
            line = self.rfile.readline(1025)
            if not line.endswith(b"\r\n") or len(line) > 1024:
                raise invalid
            size = line[:-2].split(b";", 1)[0]
            if not re.fullmatch(rb"[0-9a-fA-F]+", size):
                raise invalid
            length = int(size, 16)
            if len(body) + length > _MAX_BODY_BYTES:
                raise too_large
            if length == 0:
                self._read_chunk_trailers(invalid)
                return body
            chunk = self.rfile.read(length)
            if len(chunk) != length or self.rfile.read(2) != b"\r\n":
                raise invalid
            body.extend(chunk)

    def _read_chunk_trailers(self, invalid):
        remaining = _MAX_BODY_BYTES
        while remaining > 0:
            line = self.rfile.readline(remaining + 1)
            if line == b"\r\n":
                return
            if not line.endswith(b"\r\n") or b":" not in line:
                break
            remaining -= len(line)
        raise invalid

    def _api(self, route):
        method = _API_METHODS.get(route)
        if method is None:
            raise ApiError(404, "NOT_FOUND", "This page does not exist.")
        if self.command != method:
            raise ApiError(405, "METHOD_NOT_ALLOWED", "This request method is not supported.")

        cookies = _cookies(self.headers.get("Cookie", ""))
        digest = _token_digest(cookies.get(_SESSION_COOKIE, ""))
        now = datetime.now(timezone.utc)
        if method == "GET":
            if not digest:
                raise _unauthenticated()
            with _connection(self.server.db_path) as connection:
                workspace = _load_workspace(connection)
                user_id = _require_session(workspace, digest, now)
            self._json(Bank(workspace["bank"], now=now).dashboard(user_id))
            return

        self._check_origin()
        payload = self._read_body()
        if route == "/api/logout":
            self._logout(digest)
        elif route == "/api/action":
            self._action(payload, digest, now)
        else:
            self._authenticate(route, payload, digest, _VISIT_COOKIE in cookies, now)

    def _logout(self, digest):
        if digest:
            with _connection(self.server.db_path, write=True) as connection:
                workspace = _load_workspace(connection)
                if workspace and workspace["sessions"].pop(digest, None):
                    _save_workspace(connection, workspace)
        self._json({"message": "Signed out."}, cookies=[
            _cookie(_SESSION_COOKIE, "", 0), _cookie(_VISIT_COOKIE, "1", _VISIT_SECONDS),
        ])

    def _action(self, payload, digest, now):
        if not digest:
            raise _unauthenticated()
        alerts = []
        with _connection(self.server.db_path, write=True) as connection:
            workspace = _load_workspace(connection)
            user_id = _require_session(workspace, digest, now)
            bank = Bank(workspace["bank"], now=now, notify=alerts.append)
            outcome = bank.perform(user_id, payload)
            result = {**outcome, "dashboard": bank.dashboard(user_id)}
            _save_workspace(connection, workspace)
        for alert in alerts:
            print("[Aster simulated SMS/email]", json.dumps(alert, ensure_ascii=True), flush=True)
        self._json(result)

    def _authenticate(self, route, payload, digest, visited, now):
        bootstrap = route == "/api/bootstrap"
        if bootstrap and visited and not digest:
            raise _unauthenticated()
        cookies = []
        with _connection(self.server.db_path, write=True) as connection:
            workspace = _load_workspace(connection)
            user_id = _session_user(workspace, digest, now) if bootstrap else None
            if bootstrap and not user_id and visited:
                raise _unauthenticated()
            if workspace is None:
                workspace = {"bank": seed_bank(now), "sessions": {}}
            bank = Bank(workspace["bank"], now=now)
            if user_id is None:
                if bootstrap:
                    user_id = _DEMO_USER
                elif route == "/api/login":
                    user_id = bank.login(payload.get("email"), payload.get("credential"))["id"]
                else:
                    user_id = bank.register(payload.get("name"), payload.get("email"), payload.get("password"), payload.get("pin"))["id"]
                token = secrets.token_hex(32)
                timestamp = _timestamp_ms(now)
                workspace["sessions"] = {
                    key: session for key, session in workspace["sessions"].items()
                    if key != digest and session["expiresAt"] > timestamp
                }
                workspace["sessions"][_token_digest(token)] = {
                    "userId": user_id,
                    "expiresAt": timestamp + _SESSION_SECONDS * 1000,
                }
                _save_workspace(connection, workspace)
                cookies = [_cookie(_SESSION_COOKIE, token, _SESSION_SECONDS), _cookie(_VISIT_COOKIE, "1", _VISIT_SECONDS)]
            dashboard = bank.dashboard(user_id)
        self._json(dashboard, cookies=cookies)


def create_server(host="127.0.0.1", port=3000, db_path=DEFAULT_DB_PATH):
    """Prepare the local workspace and return an HTTP server ready to serve."""
    db_path = Path(db_path).resolve()
    _prepare_database(db_path)
    return BankServer((host, port), db_path)
