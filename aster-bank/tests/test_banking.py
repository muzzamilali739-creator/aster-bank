"""Regression coverage for the Python banking domain and local HTTP server."""

import contextlib
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from http.client import HTTPConnection
from http.cookies import SimpleCookie
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest

from aster_bank.bank import Account, Bank, BankError, FixedDepositAccount, Transaction, seed_bank
from aster_bank.server import create_server


DAY = "2026-11-23T07:00:00Z"
SAVINGS = "10003482"
CURRENT = "10007061"
FIXED_DEPOSIT = "10009123"
OMAR_SAVINGS = "10005619"
AYESHA = ("ayesha@aster.demo", "123456")
OMAR = ("omar@aster.demo", "234567")
TELLER = ("teller@aster.demo", "112233")
ADMIN = ("admin@aster.demo", "654321")


def find(items, item_id):
    return next(item for item in items if item["id"] == item_id)


def transfer(destination, amount, pin=AYESHA[1]):
    return {
        "action": "transfer", "accountId": SAVINGS, "toAccountId": destination,
        "amount": amount, "pin": pin,
    }


def adjustment(action, amount, account_id=SAVINGS, pin=AYESHA[1]):
    return {"action": action, "accountId": account_id, "amount": amount, "pin": pin}


class BankTest(unittest.TestCase):
    def setUp(self):
        self.state = seed_bank(DAY)
        self.alerts = []
        self.bank = Bank(self.state, now=DAY, notify=self.alerts.append)
        self.ayesha = self.bank.login(*AYESHA)["id"]
        self.omar = self.bank.login(*OMAR)["id"]
        self.teller = self.bank.login(*TELLER)["id"]
        self.admin = self.bank.login(*ADMIN)["id"]

    def account(self, account_id=SAVINGS, owner=None, bank=None):
        return find((bank or self.bank).dashboard(owner or self.ayesha)["accounts"], account_id)

    def require_failure(self, status, code, operation, *args):
        with self.assertRaises(BankError) as result:
            operation(*args)
        self.assertEqual(result.exception.status, status)
        self.assertEqual(result.exception.code, code)

    def test_register_with_password_and_pin(self):
        credentials = ("Samira Noor", "Samira@example.test", "BankingProject9!", "740263")
        customer = self.bank.register(*credentials)
        self.assertEqual(customer["email"], "samira@example.test")
        self.assertEqual(customer["role"], "customer")
        self.assertEqual(self.bank.dashboard(customer["id"])["accounts"], [])
        for secret in credentials[2:]:
            self.assertEqual(self.bank.login(credentials[1], secret)["id"], customer["id"])
        self.assertEqual(set(customer), {"id", "name", "email", "role"})
        self.require_failure(401, "INVALID_CREDENTIALS", self.bank.login, credentials[1], "wrong password")
        self.require_failure(409, "EMAIL_IN_USE", self.bank.register, *credentials)

    def test_transfer_to_own_and_other_customer_accounts(self):
        initial_savings = self.account()["balance"]
        initial_current = self.account(CURRENT)["balance"]
        initial_recipient = self.account(OMAR_SAVINGS, self.omar)["balance"]
        result_own = self.bank.perform(self.ayesha, transfer(CURRENT, 12_000))["transaction"]
        result_other = self.bank.perform(self.ayesha, transfer(OMAR_SAVINGS, 15_000))["transaction"]
        self.assertEqual(self.account()["balance"], initial_savings - 27_000)
        self.assertEqual(self.account(CURRENT)["balance"], initial_current + 12_000)
        self.assertEqual(self.account(OMAR_SAVINGS, self.omar)["balance"], initial_recipient + 15_000)
        self.assertEqual(sum(entry["amount"] for entry in result_other["entries"]), 0)
        self.assertEqual(find(self.bank.dashboard(self.omar)["transactions"], result_other["id"]), result_other)
        audit = self.bank.dashboard(self.admin)["audit"]
        for record in (result_own, result_other):
            self.assertTrue(any(item["transactionId"] == record["id"] for item in audit))
        recipient_notices = [item for item in self.alerts if item["accountId"] == OMAR_SAVINGS]
        self.assertEqual({item["channel"] for item in recipient_notices}, {"SMS", "Email"})
        self.assertEqual({item["transactionId"] for item in recipient_notices}, {result_other["id"]})
        self.assertEqual(self.bank.dashboard(self.ayesha)["audit"], [])

    def test_proxy_authorizes_pin_ownership_and_teller_deposits(self):
        before = deepcopy(self.bank.dashboard(self.admin))
        self.require_failure(403, "INVALID_PIN", self.bank.perform, self.ayesha, transfer(OMAR_SAVINGS, 5_000, "999999"))
        self.require_failure(403, "FORBIDDEN", self.bank.perform, self.omar, transfer(CURRENT, 5_000, OMAR[1]))
        self.require_failure(403, "FORBIDDEN", self.bank.perform, self.teller, adjustment("withdraw", 5_000, pin=TELLER[1]))
        self.assertEqual(before, self.bank.dashboard(self.admin))
        self.assertEqual(self.alerts, [])
        balance = self.account()["balance"]
        self.bank.perform(self.teller, adjustment("deposit", 5_000, pin=TELLER[1]))
        self.assertEqual(self.account()["balance"], balance + 5_000)
        self.assertNotIn("balance", self.account(owner=self.teller))

    def test_daily_limit_includes_transfer_and_resets_at_karachi_midnight(self):
        self.bank.perform(self.ayesha, transfer(OMAR_SAVINGS, 70_000))
        before = deepcopy(self.bank.dashboard(self.admin))
        request = adjustment("withdraw", 31_000)
        self.require_failure(409, "DAILY_LIMIT", self.bank.perform, self.ayesha, request)
        self.assertEqual(self.bank.dashboard(self.admin), before)

        later = Bank(self.state, now="2026-11-23T19:01:00Z")
        balance = self.account(bank=later)["balance"]
        later.perform(self.ayesha, request)
        self.assertEqual(self.account(bank=later)["balance"], balance - request["amount"])

    def test_balance_rules_fixed_deposit_lock_and_low_balance_alerts(self):
        balance = self.account(FIXED_DEPOSIT)["balance"]
        self.require_failure(409, "FUNDS_LOCKED", self.bank.perform, self.ayesha, adjustment("withdraw", 1_000, FIXED_DEPOSIT))
        self.assertEqual(self.account(FIXED_DEPOSIT)["balance"], balance)
        account = self.bank.perform(self.ayesha, {
            "action": "openAccount", "type": "savings", "name": "Rule Test Savings", "pin": AYESHA[1],
        })["account"]
        amount = account["minBalance"] + 5_000
        account_id = account["id"]
        self.bank.perform(self.ayesha, adjustment("deposit", amount, account_id))
        notices_before = len(self.alerts)
        self.require_failure(409, "INSUFFICIENT_FUNDS", self.bank.perform, self.ayesha, adjustment("withdraw", amount + 1, account_id))
        self.require_failure(409, "MINIMUM_BALANCE", self.bank.perform, self.ayesha, adjustment("withdraw", amount - 1, account_id))
        self.assertEqual(self.account(account_id)["balance"], amount)
        self.assertEqual(len(self.alerts), notices_before)
        self.bank.perform(self.ayesha, adjustment("withdraw", 5_000, account_id))
        self.assertEqual(self.account(account_id)["balance"], account["minBalance"])
        low_alerts = [item for item in self.alerts if item["accountId"] == account_id and item["type"] == "lowBalance"]
        self.assertEqual(sorted(item["channel"] for item in low_alerts), ["Email", "SMS"])

    def test_admin_undo_each_command_once_and_restores_daily_allowance(self):
        commands = (adjustment("deposit", 7_000), adjustment("withdraw", 7_000), transfer(OMAR_SAVINGS, 7_000))
        for command in commands:
            with self.subTest(command=command["action"]):
                before = self.account()
                recipient_balance = self.account(OMAR_SAVINGS, self.omar)["balance"]
                transaction = self.bank.perform(self.ayesha, command)["transaction"]
                request = {"action": "reverse", "transactionId": transaction["id"], "pin": AYESHA[1]}
                self.require_failure(403, "FORBIDDEN", self.bank.perform, self.ayesha, request)
                request["pin"] = ADMIN[1]
                reversal = self.bank.perform(self.admin, request)["transaction"]
                self.assertEqual(reversal["reversalOf"], transaction["id"])
                self.assertEqual(self.account()["balance"], before["balance"])
                self.assertEqual(self.account()["dailyRemaining"], before["dailyRemaining"])
                self.assertEqual(self.account(OMAR_SAVINGS, self.omar)["balance"], recipient_balance)
                after = deepcopy(self.bank.dashboard(self.admin))
                self.assertIsNotNone(find(after["transactions"], transaction["id"])["reversedAt"])
                self.assertTrue(any(
                    item["transactionId"] == reversal["id"] and item["action"] == "reversal"
                    for item in after["audit"]
                ))
                self.require_failure(409, "ALREADY_REVERSED", self.bank.perform, self.admin, request)
                self.assertEqual(after, self.bank.dashboard(self.admin))

    def test_failed_transfer_reversal_has_no_partial_effects(self):
        recipient = self.bank.perform(self.omar, {
            "action": "openAccount", "type": "current", "name": "New Current", "pin": OMAR[1],
        })["account"]["id"]
        transaction = self.bank.perform(self.ayesha, transfer(recipient, 50_000))["transaction"]
        self.bank.perform(self.omar, adjustment("withdraw", 50_000, recipient, OMAR[1]))
        before = deepcopy(self.bank.dashboard(self.admin))
        alert_count = len(self.alerts)
        request = {"action": "reverse", "transactionId": transaction["id"], "pin": ADMIN[1]}
        self.require_failure(409, "INSUFFICIENT_FUNDS", self.bank.perform, self.admin, request)
        self.assertEqual(before, self.bank.dashboard(self.admin))
        self.assertEqual(alert_count, len(self.alerts))

    def test_month_end_interest_fees_and_reconciled_statements(self):
        month = "2026-11"
        savings = self.account()
        current = self.account(CURRENT)
        request = {"action": "monthEnd", "month": month, "pin": AYESHA[1]}
        self.require_failure(403, "FORBIDDEN", self.bank.perform, self.ayesha, request)
        request["pin"] = ADMIN[1]
        before = self.bank.dashboard(self.ayesha)
        self.bank.perform(self.admin, request)
        after = deepcopy(self.bank.dashboard(self.ayesha))
        statements = {item["accountId"]: item for item in after["monthlyStatements"] if item["month"] == month}
        interest = (savings["balance"] + 200) // 400
        self.assertEqual(statements[SAVINGS]["interest"], interest)
        self.assertEqual(statements[SAVINGS]["fee"], 0)
        self.assertEqual(statements[SAVINGS]["closingBalance"], savings["balance"] + interest)
        self.assertEqual(statements[CURRENT]["interest"], 0)
        self.assertEqual(statements[CURRENT]["fee"], current["monthlyFee"])
        self.assertEqual(statements[CURRENT]["closingBalance"], current["balance"] - current["monthlyFee"])
        for account_id in (SAVINGS, CURRENT):
            opening = sum(
                leg["amount"] for item in before["transactions"] if item["date"] < month + "-01"
                for leg in item["entries"] if leg["accountId"] == account_id
            )
            self.assertEqual(statements[account_id]["openingBalance"], opening)
            self.assertEqual(statements[account_id]["closingBalance"], self.account(account_id)["balance"])
        self.require_failure(409, "MONTH_ALREADY_PROCESSED", self.bank.perform, self.admin, request)
        self.assertEqual(after, self.bank.dashboard(self.ayesha))

    def test_abstract_contracts_and_month_end_order(self):
        with self.assertRaises(TypeError):
            Account({})
        with self.assertRaises(TypeError):
            Transaction(None, 100)
        steps = []

        class TemplateProbe(Account):
            def withdraw(self, amount, **options):
                return super().withdraw(amount, **options)

            def calculate_interest(self, balance):
                steps.append(("calculate_interest", balance))
                return 2_000

            def apply_fees(self, balance, post):
                steps.append(("apply_fees", balance))
                post("fee", 1_000)
                return 1_000

        concrete = TemplateProbe({
            "id": "probe", "ownerId": self.ayesha, "name": "Probe", "type": "savings",
            "balance": 100_000, "createdOn": "2026-11-01",
        })
        with self.assertRaises(AttributeError):
            concrete.balance = 0

        def generate_statement(*, interest, fee):
            steps.append(("generate_statement", interest, fee))
            return "statement"

        self.assertEqual(concrete.process_month_end(
            balance=concrete.balance,
            post=lambda action, amount: steps.append((action, amount)),
            generate_statement=generate_statement,
        ), "statement")
        self.assertEqual(steps, [
            ("calculate_interest", 100_000), ("interest", 2_000), ("apply_fees", 100_000),
            ("fee", 1_000), ("generate_statement", 2_000, 1_000),
        ])

    def test_direct_fixed_deposit_withdrawal_validates_maturity_and_cents(self):
        record = {
            "id": "fd-probe", "ownerId": self.ayesha, "name": "Fixed", "type": "fixed",
            "balance": 100_000, "createdOn": "2000-01-01",
        }
        locked = FixedDepositAccount({**record, "maturesOn": "9999-12-31"})
        self.require_failure(409, "FUNDS_LOCKED", locked.withdraw, 100)
        self.assertEqual(locked.balance, record["balance"])
        matured = FixedDepositAccount({**record, "maturesOn": "2000-04-01"})
        for invalid in (0, -1, True, 0.01):
            with self.subTest(invalid=invalid):
                self.require_failure(400, "INVALID_AMOUNT", matured.withdraw, invalid)
        matured.withdraw(100)
        self.assertEqual(matured.balance, record["balance"] - 100)


@contextlib.contextmanager
def running_server(db_path):
    with create_server("127.0.0.1", 0, db_path) as server:
        runner = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        runner.start()
        try:
            yield server.server_address[1]
        finally:
            server.shutdown()
            runner.join(timeout=3)


class ApiClient:
    def __init__(self, port):
        self.port = port
        self.cookies = {}

    def send(self, route, body=None, *, origin=None, alternate_cookies=None):
        headers = {"Cookie": "; ".join(f"{key}={value}" for key, value in (
            self.cookies if alternate_cookies is None else alternate_cookies
        ).items())}
        if body is not None:
            headers["Content-Type"] = "application/json"
            headers["Origin"] = origin or f"http://127.0.0.1:{self.port}"
        client = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            client.request("GET" if body is None else "POST", f"/api/{route}",
                           body=None if body is None else json.dumps(body), headers=headers)
            response = client.getresponse()
            cookie_headers = [value for name, value in response.getheaders() if name.lower() == "set-cookie"]
            for cookie_header in cookie_headers:
                parsed = SimpleCookie()
                parsed.load(cookie_header)
                for name, cookie in parsed.items():
                    if cookie["max-age"] == "0":
                        self.cookies.pop(name, None)
                    else:
                        self.cookies[name] = cookie.value
            return response.status, json.loads(response.read()), cookie_headers
        finally:
            client.close()


class ApiTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.db_path = Path(temporary.name) / "aster-test.sqlite3"

    def test_http_session_rotation_logout_origin_checks_and_sqlite_restart(self):
        with running_server(self.db_path) as port:
            client = ApiClient(port)
            self.assertEqual(client.send("dashboard")[0], 401)
            status, sample, headers = client.send("bootstrap", {})
            self.assertEqual(status, 200)
            self.assertEqual(sample["user"]["email"], AYESHA[0])
            session_header = next(item for item in headers if "aster_session=" in item)
            self.assertRegex(session_header, r"aster_session=[0-9a-f]{64};")
            self.assertIn("HttpOnly", session_header)
            self.assertIn("SameSite=Strict", session_header)
            stale_cookies = dict(client.cookies)
            status, _, _ = client.send("login", {"email": AYESHA[0], "credential": "AsterDemo1!"})
            self.assertEqual(status, 200)
            self.assertNotEqual(stale_cookies, client.cookies)
            self.assertEqual(client.send("dashboard", alternate_cookies=stale_cookies)[0], 401)

            self.assertEqual(client.send("action", transfer(OMAR_SAVINGS, 100), origin="https://elsewhere.test")[0], 403)
            status, denied, _ = client.send("action", transfer(OMAR_SAVINGS, 100, "999999"))
            self.assertEqual((status, denied["code"]), (403, "INVALID_PIN"))
            status, operation, _ = client.send("action", transfer(OMAR_SAVINGS, 10_000))
            self.assertEqual(status, 200)
            transfer_id = operation["transaction"]["id"]
            final_balance = find(operation["dashboard"]["accounts"], SAVINGS)["balance"]
            self.assertEqual(final_balance, find(sample["accounts"], SAVINGS)["balance"] - 10_000)

            self.assertEqual(client.send("logout", {})[0], 200)
            self.assertEqual(client.send("dashboard")[0], 401)
            self.assertEqual(client.send("bootstrap", {})[0], 401)

        with running_server(self.db_path) as port:
            client = ApiClient(port)
            status, restored, _ = client.send("login", {"email": AYESHA[0], "credential": AYESHA[1]})
            self.assertEqual(status, 200)
            self.assertEqual(find(restored["accounts"], SAVINGS)["balance"], final_balance)
            self.assertEqual(find(restored["transactions"], transfer_id)["type"], "transfer")

    def test_registration_creates_only_customer_sessions(self):
        with running_server(self.db_path) as port:
            client = ApiClient(port)
            status, data, _ = client.send("register", {
                "name": "New Customer", "email": "new@example.test", "password": "DemoSignup9!",
                "pin": "765321", "role": "admin",
            })
            self.assertIn(status, (200, 201))
            self.assertEqual(data["user"]["role"], "customer")
            self.assertEqual(client.send("dashboard")[1]["user"], data["user"])
            status, denial, _ = client.send("action", {"action": "reverse", "pin": "765321", "transactionId": "TX-1"})
            self.assertEqual((status, denial["code"]), (403, "FORBIDDEN"))

    def test_concurrent_http_withdrawals_commit_one_command(self):
        with running_server(self.db_path) as port:
            first = ApiClient(port)
            second = ApiClient(port)
            status, initial, _ = first.send("bootstrap", {})
            self.assertEqual(status, 200)
            self.assertEqual(second.send("login", {"email": AYESHA[0], "credential": AYESHA[1]})[0], 200)
            withdrawal = adjustment("withdraw", 70_000)
            with ThreadPoolExecutor(max_workers=2) as pool:
                responses = list(pool.map(lambda client: client.send("action", withdrawal), (first, second)))
            self.assertEqual(sorted(response[0] for response in responses), [200, 409])
            invalid = next(response[1] for response in responses if response[0] == 409)
            self.assertEqual(invalid["code"], "DAILY_LIMIT")
            valid = next(response[1] for response in responses if response[0] == 200)
            status, current, _ = first.send("dashboard")
            self.assertEqual(status, 200)
            self.assertEqual(find(current["accounts"], SAVINGS)["balance"], find(initial["accounts"], SAVINGS)["balance"] - 70_000)
            initial_ids = {record["id"] for record in initial["transactions"]}
            transaction_id = valid["transaction"]["id"]
            self.assertEqual([record["id"] for record in current["transactions"] if record["id"] not in initial_ids], [transaction_id])
            notices = [item for item in current["notifications"] if item["transactionId"] == transaction_id]
            self.assertEqual(sorted(item["channel"] for item in notices), ["Email", "SMS"])


if __name__ == "__main__":
    unittest.main()
