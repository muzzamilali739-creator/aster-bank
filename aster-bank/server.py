"""Launch the local Aster Bank Python server."""

import argparse
import os
import sys
from pathlib import Path


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("Aster Bank requires Python 3.10 or newer.")

    from aster_bank.server import create_server

    parser = argparse.ArgumentParser(description="Run the Aster Bank banking sandbox.")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=os.environ.get("PORT", "3000"))
    parser.add_argument("--db", type=Path, default=Path(__file__).resolve().parent / ".data" / "bank.sqlite")
    args = parser.parse_args()

    with create_server(args.host, args.port, args.db) as server:
        host, port = server.server_address[:2]
        print(f"Aster Bank is running at http://{host}:{port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nAster Bank stopped.")


if __name__ == "__main__":
    main()
