"""Banking domain, shared by the desktop UI and its HTTP endpoints.

Python objects implement the account rules and patterns. Persisted state and
API responses use the JSON field names consumed by the desktop frontend.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from calendar import monthrange
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import pbkdf2_hmac
from hmac import compare_digest
import re
from secrets import token_hex
from typing import final
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


try:
    _BUSINESS_ZONE = ZoneInfo("Asia/Karachi")
except ZoneInfoNotFoundError:
    # Current Pakistan Standard Time on systems without an IANA time-zone database.
    _BUSINESS_ZONE = timezone(timedelta(hours=5), "PKT")

_PIN = re.compile(r"[0-9]{6}")
_EMAIL = re.compile(r"[^\s@]+@[^\s@]+\.[^\s@]+")
_MONTH = re.compile(r"[1-9][0-9]{3}-(0[1-9]|1[0-2])")
_MAX_CENTS = 2**53 - 1
_CREDENTIAL_ITERATIONS = 80_000
_REVERSAL = object()
_SERVICE_FEE = object()


@dataclass(frozen=True)
class AccountRules:
    name: str
    min_balance: int
    daily_limit: int
    low_balance: int
    monthly_rate: float = 0
    monthly_fee: int = 0
    term_days: int = 0


_RULES = {
    "savings": AccountRules("Savings", 10_000, 100_000, 25_000, monthly_rate=0.0025),
    "current": AccountRules("Current", 0, 200_000, 20_000, monthly_fee=1_200),
    "fixed": AccountRules("Fixed Deposit", 0, 500_000, 0, term_days=90),
}


class BankError(Exception):
    def __init__(self, message: str, code: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.status = status


def _clock(value: datetime | str | None = None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    if isinstance(value, str):
        value = datetime.fromisoformat(value.removesuffix("Z") + "+00:00" if value.endswith("Z") else value)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _day_of(value: datetime) -> str:
    return value.astimezone(_BUSINESS_ZONE).date().isoformat()


def _timestamp(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _amount_in_cents(value: object) -> int:
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    if type(value) is not int or not 0 < value <= _MAX_CENTS:
        raise BankError("Enter a positive amount with at most two decimal places.", "INVALID_AMOUNT")
    return value


def _dollars(cents: int) -> str:
    dollars, remainder = divmod(abs(cents), 100)
    prefix = "-$" if cents < 0 else "$"
    return f"{prefix}{dollars:,}.{remainder:02d}"


def _digest(credential: str, salt: str) -> str:
    # Match UTF-8 encoding and salted PBKDF2 records used by the existing data.
    text = credential.encode("utf-16-le", "surrogatepass").decode("utf-16-le", "replace")
    return pbkdf2_hmac(
        "sha256", text.encode("utf-8"), bytes.fromhex(salt), _CREDENTIAL_ITERATIONS, dklen=32
    ).hex()


def _hash_credential(credential: str) -> dict:
    salt = token_hex(16)
    return {"salt": salt, "digest": _digest(credential, salt)}


def _verify_credential(credential: str, record: dict) -> bool:
    return compare_digest(_digest(credential, record["salt"]), record["digest"])


def _credential_record(values: tuple[str, str]) -> dict:
    return {"salt": values[0], "digest": values[1]}


# Independently salted hashes for the documented demo accounts.
_DEMO_USERS = (
    (
        "customer-ayesha", "Ayesha Khan", "ayesha@aster.demo", "customer",
        ("445a17a5385d258e90528dc8034594a8", "a4731971260d69fdecf079a269bd45e0084a2035fc5846e5a8c9f991aedf8c03"),
        ("bd299fb1b8e378186217eb0e1eece12a", "7f10c9c7bf03a497b58b60e49517a4eb59f8cc29781dac7b3a5f7bcd18d6779b"),
    ),
    (
        "customer-omar", "Omar Malik", "omar@aster.demo", "customer",
        ("6edcdbb2c95ea9d48d495d07e87f3c45", "fff27f65c51656d2922c204a7fc784b67fc9e2d8b9cd4d574b66206e6258d261"),
        ("dd7520f37e610052686bc043aaaa2512", "6f0fc4692d983b9f867feb0e69ef889257888a3676fa4311b7bb2525c3c82fca"),
    ),
    (
        "admin-demo", "Sara Ahmed", "admin@aster.demo", "admin",
        ("62b25aab5e70bdd5ec6caff667a74ebf", "e66b8aad4bdb6e6f3159a37db7dd1345091d8cfb692f6a9921269ff5bd53f353"),
        ("a604a0a4aa4a4201f3232c399fb2398d", "a6f5fc5cd53b647845da6f1d1ea7816a430615ef6e5105f47c68bcb52c016475"),
    ),
    (
        "teller-demo", "Hamza Ali", "teller@aster.demo", "teller",
        ("2128dc05679274cd4407d82fbe685642", "d29b7625010f7f9ac465bf91ae889fbc208f06a2dff151b99eb42f11b6dbb3df"),
        ("6adf3935c9cc5c31514628ddbebb8458", "e7fe560de66094fb25b4871b8b005e6ea16b4f1432bf1bc97b779cf74fb03ddb"),
    ),
)


def _public_user(user: dict) -> dict:
    return {key: user[key] for key in ("id", "name", "email", "role")}


class Account(ABC):
    """An account with a private balance and an account-specific withdrawal policy."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "process_month_end" in cls.__dict__:
            raise TypeError("Override calculate_interest or apply_fees to customize month-end.")

    def __init__(self, record: dict):
        self.id = record["id"]
        self.owner_id = record["ownerId"]
        self.name = record["name"]
        self.type = record["type"]
        self.created_on = record["createdOn"]
        self.matures_on = record.get("maturesOn")
        self.__balance = record["balance"]
        self.__daily_spent = dict(record.get("dailySpent", {}))

    @property
    def balance(self) -> int:
        return self.__balance

    @property
    def rules(self) -> AccountRules:
        return _RULES[self.type]

    def remaining_on(self, day: str) -> int:
        return max(0, self.rules.daily_limit - self.__daily_spent.get(day, 0))

    def deposit(self, amount: int, *, verify_only=False, operation=None, original_day=None) -> None:
        amount = _amount_in_cents(amount)
        if self.__balance + amount > _MAX_CENTS:
            raise BankError("The resulting balance exceeds the maximum supported amount.", "BALANCE_LIMIT")
        if verify_only:
            return
        self.__balance += amount
        if operation is _REVERSAL and original_day:
            spent = self.__daily_spent.get(original_day, 0)
            self.__daily_spent[original_day] = max(0, spent - amount)

    @abstractmethod
    def withdraw(self, amount: int, *, day=None, verify_only=False, operation=None) -> None:
        """Apply this account's withdrawal policy before debiting the balance."""

    def _withdraw(self, amount, *, day, min_balance, verify_only, operation) -> None:
        amount = _amount_in_cents(amount)
        day = day or _day_of(_clock())
        privileged = operation is _REVERSAL or operation is _SERVICE_FEE
        if amount > self.__balance:
            raise BankError("Insufficient funds for this transaction.", "INSUFFICIENT_FUNDS", 409)
        if not privileged and amount > self.remaining_on(day):
            remaining = _dollars(self.remaining_on(day))
            daily_limit = _dollars(self.rules.daily_limit)
            raise BankError(
                f"Daily withdrawal limit exceeded. {remaining} is available today from the {daily_limit} daily limit.",
                "DAILY_LIMIT", 409,
            )
        if not privileged and self.__balance - amount < min_balance:
            raise BankError(f"Keep at least {_dollars(min_balance)} in this account.", "MINIMUM_BALANCE", 409)
        if verify_only:
            return
        self.__balance -= amount
        if not privileged:
            self.__daily_spent[day] = self.__daily_spent.get(day, 0) + amount

    @final
    def process_month_end(self, *, balance, post, generate_statement):
        """Template Method. Calculate interest, apply fees, then generate the statement."""
        interest = self.calculate_interest(balance)
        if interest:
            post("interest", interest)
        fee = self.apply_fees(balance, post)
        return generate_statement(interest=interest, fee=fee)

    def calculate_interest(self, balance: int) -> int:
        return 0

    def apply_fees(self, balance: int, post) -> int:
        return 0

    def snapshot(self) -> dict:
        return {
            "id": self.id, "ownerId": self.owner_id, "name": self.name, "type": self.type,
            "balance": self.__balance, "dailySpent": dict(self.__daily_spent),
            "createdOn": self.created_on, "maturesOn": self.matures_on,
        }


class SavingsAccount(Account):
    def withdraw(self, amount, *, day=None, verify_only=False, operation=None) -> None:
        self._withdraw(
            amount, day=day, min_balance=self.rules.min_balance, verify_only=verify_only, operation=operation
        )

    def calculate_interest(self, balance: int) -> int:
        # 0.25% of the balance, rounded to cents with half cents rounded up.
        return (max(0, balance) + 200) // 400


class CurrentAccount(Account):
    def withdraw(self, amount, *, day=None, verify_only=False, operation=None) -> None:
        self._withdraw(amount, day=day, min_balance=0, verify_only=verify_only, operation=operation)

    def apply_fees(self, balance: int, post) -> int:
        fee = self.rules.monthly_fee
        if min(balance, self.balance) < fee:
            return 0
        post("fee", fee)
        return fee


class FixedDepositAccount(Account):
    def withdraw(self, amount, *, day=None, verify_only=False, operation=None) -> None:
        day = day or _day_of(_clock())
        if operation is not _REVERSAL and self.matures_on and day < self.matures_on:
            raise BankError(f"Fixed deposits are locked until {self.matures_on}.", "FUNDS_LOCKED", 409)
        self._withdraw(amount, day=day, min_balance=0, verify_only=verify_only, operation=operation)


_ACCOUNT_TYPES = {"savings": SavingsAccount, "current": CurrentAccount, "fixed": FixedDepositAccount}


def _entry(account: Account, amount: int) -> dict:
    return {"accountId": account.id, "amount": amount}


class Transaction(ABC):
    """A command that returns its signed ledger entries on execute or undo."""

    def __init__(self, account: Account, amount: int):
        self.account = account
        self.amount = _amount_in_cents(amount)

    @abstractmethod
    def execute(self, *, day=None) -> list[dict]:
        """Post the command's balance changes."""

    @abstractmethod
    def undo(self, *, original_day=None) -> list[dict]:
        """Post compensating balance changes for the saved command."""


class Deposit(Transaction):
    def execute(self, *, day=None) -> list[dict]:
        self.account.deposit(self.amount)
        return [_entry(self.account, self.amount)]

    def undo(self, *, original_day=None) -> list[dict]:
        self.account.withdraw(self.amount, operation=_REVERSAL)
        return [_entry(self.account, -self.amount)]


class Withdraw(Transaction):
    def execute(self, *, day=None) -> list[dict]:
        self.account.withdraw(self.amount, day=day)
        return [_entry(self.account, -self.amount)]

    def undo(self, *, original_day=None) -> list[dict]:
        self.account.deposit(self.amount, operation=_REVERSAL, original_day=original_day)
        return [_entry(self.account, self.amount)]


class Transfer(Transaction):
    def __init__(self, source: Account, destination: Account, amount: int):
        super().__init__(source, amount)
        if source.id == destination.id:
            raise BankError("Choose a different destination account.", "SAME_ACCOUNT")
        self.destination = destination

    def execute(self, *, day=None) -> list[dict]:
        self.destination.deposit(self.amount, verify_only=True)
        self.account.withdraw(self.amount, day=day)
        self.destination.deposit(self.amount)
        return [_entry(self.account, -self.amount), _entry(self.destination, self.amount)]

    def undo(self, *, original_day=None) -> list[dict]:
        self.account.deposit(self.amount, verify_only=True)
        self.destination.withdraw(self.amount, operation=_REVERSAL)
        self.account.deposit(self.amount, operation=_REVERSAL, original_day=original_day)
        return [_entry(self.account, self.amount), _entry(self.destination, -self.amount)]


_COMMANDS = {"deposit": Deposit, "withdraw": Withdraw, "transfer": Transfer}
_DESCRIPTIONS = {
    "deposit": "Cash deposit", "withdraw": "Cash withdrawal",
    "interest": "Savings interest", "fee": "Monthly service fee",
}
_COMPLETION_MESSAGES = {
    "deposit": "Deposit completed.", "withdraw": "Withdrawal completed.", "transfer": "Transfer completed.",
}


class AccountProxy:
    """Protection Proxy for account access and staff operations."""

    def __init__(self, actor: dict, account: Account | None = None):
        self.__actor = actor
        self.__account = account

    def execute(self, action, pin, operation):
        self._authorize(action, pin)
        return operation(self.__account)

    def _authorize(self, action, pin) -> None:
        role = self.__actor["role"]
        owner = self.__account is not None and self.__account.owner_id == self.__actor["id"]
        authorized = False
        if action in _COMMANDS:
            authorized = (role == "customer" and owner) or (role == "teller" and action == "deposit")
        elif action == "openAccount":
            authorized = role == "customer"
        elif action in ("reverse", "monthEnd"):
            authorized = role == "admin"
        if not authorized:
            raise BankError("You are not authorized to perform this operation.", "FORBIDDEN", 403)
        if not isinstance(pin, str) or not _PIN.fullmatch(pin) or not _verify_credential(pin, self.__actor["pinHash"]):
            raise BankError("Incorrect PIN. The account operation was blocked.", "INVALID_PIN", 403)


class TransactionPublisher:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer) -> None:
        self._observers.append(observer)

    def publish(self, transaction: dict, account: Account, amount: int) -> None:
        for observer in self._observers:
            observer.update(transaction, account, amount)


class NotificationService:
    def __init__(self, notifications: list, notify):
        self._notifications = notifications
        self._notify = notify

    def send(self, transaction, account, kind, message) -> None:
        for channel in ("SMS", "Email"):
            alert = {
                "id": f"{transaction['id']}-{account.id}-{kind}-{channel.lower()}",
                "at": transaction["at"], "message": message, "channel": channel, "type": kind,
                "accountId": account.id, "transactionId": transaction["id"], "userId": account.owner_id,
            }
            self._notifications.append(alert)
            if self._notify is not None:
                self._notify(alert)


class TransactionObserver:
    def __init__(self, service: NotificationService):
        self._service = service

    def update(self, transaction, account, amount) -> None:
        movement = "credited to" if amount > 0 else "debited from"
        message = f"{_dollars(abs(amount))} {movement} {account.name}. {transaction['description']}."
        self._service.send(transaction, account, "transaction", message)


class LowBalanceObserver:
    def __init__(self, service: NotificationService):
        self._service = service

    def update(self, transaction, account, amount) -> None:
        if amount < 0 and account.balance < account.rules.low_balance:
            message = f"{account.name} has a low balance of {_dollars(account.balance)}."
            self._service.send(transaction, account, "lowBalance", message)


def _newest_first(records):
    return sorted(records, key=lambda record: (record["at"], record["id"]), reverse=True)


class Bank:
    def __init__(self, state: dict, now: datetime | str | None = None, notify=None):
        self.state = state
        self.now = _clock(now)
        self.day = _day_of(self.now)
        self._accounts = {record["id"]: _ACCOUNT_TYPES[record["type"]](record) for record in state["accounts"]}
        notifications = NotificationService(state["notifications"], notify)
        self._publisher = TransactionPublisher()
        self._publisher.subscribe(TransactionObserver(notifications))
        self._publisher.subscribe(LowBalanceObserver(notifications))

    def login(self, email=None, credential=None) -> dict:
        if not isinstance(credential, str) or not 0 < len(credential) <= 128:
            raise BankError("Enter your email and password or PIN.", "INVALID_CREDENTIALS", 401)
        address = email.strip().lower() if isinstance(email, str) else ""
        user = next((candidate for candidate in self.state["users"] if candidate["email"] == address), None)
        if _PIN.fullmatch(credential):
            field = "pinHash"
            fallback = _DEMO_USERS[0][5]
        else:
            field = "passwordHash"
            fallback = _DEMO_USERS[0][4]
        matches = _verify_credential(credential, user[field] if user else _credential_record(fallback))
        if not user or not matches:
            raise BankError("Email, password, or PIN is incorrect.", "INVALID_CREDENTIALS", 401)
        return _public_user(user)

    def register(self, name=None, email=None, password=None, pin=None) -> dict:
        name = name.strip() if isinstance(name, str) else ""
        address = email.strip().lower() if isinstance(email, str) else ""
        if not name or len(name) > 80:
            raise BankError("Enter a name of up to 80 characters.", "INVALID_NAME")
        if len(address) > 254 or not _EMAIL.fullmatch(address):
            raise BankError("Enter a valid email address.", "INVALID_EMAIL")
        if not isinstance(password, str) or not 8 <= len(password) <= 128:
            raise BankError("Use a password between 8 and 128 characters.", "INVALID_PASSWORD")
        if not isinstance(pin, str) or not _PIN.fullmatch(pin):
            raise BankError("Choose a six-digit PIN.", "INVALID_PIN")
        if any(user["email"] == address for user in self.state["users"]):
            raise BankError("An account with this email already exists.", "EMAIL_IN_USE", 409)
        user = {
            "id": str(uuid4()), "name": name, "email": address, "role": "customer",
            "passwordHash": _hash_credential(password), "pinHash": _hash_credential(pin),
        }
        self.state["users"].append(user)
        self._audit(user, "register", "Customer registered")
        return _public_user(user)

    def dashboard(self, user_id: str) -> dict:
        user = self._user(user_id)
        role = user["role"]
        accounts = [
            account for account in self._accounts.values() if role != "customer" or account.owner_id == user_id
        ]
        visible_accounts = {account.id for account in accounts}
        transactions = self.state["transactions"]
        if role == "teller":
            transactions = [transaction for transaction in transactions if transaction["actorId"] == user_id]
        elif role == "customer":
            transactions = [
                transaction for transaction in transactions
                if any(entry["accountId"] in visible_accounts for entry in transaction["entries"])
            ]
        notifications = _newest_first(alert for alert in self.state["notifications"] if alert["userId"] == user_id)
        statements = [
            statement for statement in self.state["monthlyStatements"]
            if role != "teller" and statement["accountId"] in visible_accounts
        ]
        statements.sort(key=lambda statement: statement["accountId"])
        statements.sort(key=lambda statement: statement["month"], reverse=True)
        return {
            "user": _public_user(user), "accounts": [self._account_view(account, user) for account in accounts],
            "transactions": _newest_first(transactions),
            "notifications": [{key: value for key, value in alert.items() if key != "userId"} for alert in notifications],
            "monthlyStatements": statements, "audit": _newest_first(self.state["audit"]) if role == "admin" else [],
        }

    def perform(self, user_id: str, body: dict) -> dict:
        actor = self._user(user_id)
        action = body.get("action")
        if not isinstance(action, str):
            raise BankError("You are not authorized to perform this operation.", "FORBIDDEN", 403)
        pin = body.get("pin")
        if action in _COMMANDS:
            proxy = AccountProxy(actor, self._account(body.get("accountId")))
            return proxy.execute(action, pin, lambda account: self._perform_command(actor, action, account, body))
        staff_or_open = {
            "reverse": lambda: self._reverse(actor, body.get("transactionId")),
            "monthEnd": lambda: self._process_month_end(actor, body.get("month")),
            "openAccount": lambda: self._open_account(actor, body.get("type"), body.get("name")),
        }
        return AccountProxy(actor).execute(action, pin, lambda _account: staff_or_open[action]())

    def _perform_command(self, actor, action, account, body) -> dict:
        destination = self._account(body.get("toAccountId")) if action == "transfer" else None
        command = self._command(action, account, destination, body.get("amount"))
        if destination is None:
            description = _DESCRIPTIONS[action]
        else:
            recipient = destination.name if destination.owner_id == actor["id"] else self._user(destination.owner_id)["name"]
            description = f"Transfer to {recipient}"
        transaction = self._execute(actor, action, command, description)
        return {"message": _COMPLETION_MESSAGES[action], "transaction": transaction}

    def _user(self, user_id) -> dict:
        user = next((candidate for candidate in self.state["users"] if candidate["id"] == user_id), None)
        if user is None:
            raise BankError("Sign in to continue.", "AUTH_REQUIRED", 401)
        return user

    def _account(self, account_id) -> Account:
        if isinstance(account_id, str):
            key = account_id.strip()
        elif type(account_id) is int and abs(account_id) <= _MAX_CENTS:
            key = str(account_id)
        else:
            key = ""
        account = self._accounts.get(key)
        if account is None:
            raise BankError("Account number could not be found.", "ACCOUNT_NOT_FOUND", 404)
        return account

    def _account_view(self, account: Account, user: dict) -> dict:
        summary = {
            "id": account.id, "ownerId": account.owner_id, "ownerName": self._user(account.owner_id)["name"],
            "name": account.name, "type": account.type,
        }
        if user["role"] == "teller":
            return summary
        rules = account.rules
        locked = account.matures_on and self.day < account.matures_on
        return {
            **summary, "balance": account.balance, "minBalance": rules.min_balance, "dailyLimit": rules.daily_limit,
            "dailyRemaining": 0 if locked else account.remaining_on(self.day), "maturesOn": account.matures_on,
            "monthlyRate": rules.monthly_rate, "monthlyFee": rules.monthly_fee,
        }

    def _open_account(self, actor, account_type, name) -> dict:
        if not isinstance(account_type, str) or account_type not in _ACCOUNT_TYPES:
            raise BankError("Choose a valid account type.", "INVALID_ACCOUNT_TYPE")
        name = name.strip() if isinstance(name, str) else ""
        if len(name) > 48:
            raise BankError("Use an account name up to 48 characters.", "INVALID_NAME")
        rules = _RULES[account_type]
        self.state["accountSequence"] += 1
        account = _ACCOUNT_TYPES[account_type]({
            "id": str(self.state["accountSequence"]), "ownerId": actor["id"], "name": name or f"{rules.name} Account",
            "type": account_type, "balance": 0, "createdOn": self.day,
            "maturesOn": _day_of(self.now + timedelta(days=rules.term_days)) if rules.term_days else None,
        })
        self._accounts[account.id] = account
        self.state["accounts"].append(account.snapshot())
        self._audit(actor, "openAccount", f"{account.name} opened ({account.id})")
        return {"message": "Account opened.", "account": self._account_view(account, actor)}

    @staticmethod
    def _command(kind, source, destination, amount) -> Transaction:
        if kind == "transfer":
            return Transfer(source, destination, amount)
        return _COMMANDS[kind](source, amount)

    def _execute(self, actor, kind, command, description) -> dict:
        return self._post(actor, kind, description, command.execute(day=self.day))

    def _post(self, actor, kind, description, entries, *, reversal_of=None, effective_date=None) -> dict:
        self.state["transactionSequence"] += 1
        transaction = {
            "id": f"TX-{self.state['transactionSequence']}", "type": kind, "at": _timestamp(self.now),
            "date": effective_date or self.day, "description": description, "entries": entries,
            "actorId": actor["id"], "reversedAt": None, "reversalOf": reversal_of,
        }
        self.state["transactions"].append(transaction)
        for entry in entries:
            account = self._account(entry["accountId"])
            index = next(i for i, record in enumerate(self.state["accounts"]) if record["id"] == account.id)
            self.state["accounts"][index] = account.snapshot()
            self._publisher.publish(transaction, account, entry["amount"])
        self._audit(actor, kind, description, transaction["id"])
        return transaction

    def _audit(self, actor, action, description, transaction_id=None) -> None:
        self.state["auditSequence"] += 1
        self.state["audit"].append({
            "id": f"AUD-{self.state['auditSequence']}", "at": _timestamp(self.now), "actorId": actor["id"],
            "action": action, "transactionId": transaction_id, "description": description,
        })

    def _reverse(self, actor, transaction_id) -> dict:
        original = next((item for item in self.state["transactions"] if item["id"] == transaction_id), None)
        if original is None:
            raise BankError("Transaction could not be found.", "TRANSACTION_NOT_FOUND", 404)
        if original["type"] not in _COMMANDS:
            raise BankError("Only deposits, withdrawals, and transfers can be reversed.", "NOT_REVERSIBLE", 409)
        if original["reversedAt"]:
            raise BankError("This transaction has already been reversed.", "ALREADY_REVERSED", 409)
        first, *others = original["entries"]
        destination = self._account(others[0]["accountId"]) if others else None
        command = self._command(original["type"], self._account(first["accountId"]), destination, abs(first["amount"]))
        entries = command.undo(original_day=original["date"])
        description = f"Reversal of {original['id']}: {original['description']}"
        transaction = self._post(actor, "reversal", description, entries, reversal_of=original["id"])
        original["reversedAt"] = transaction["at"]
        return {"message": f"Transaction {original['id']} reversed.", "transaction": transaction}

    def _balance_through(self, account_id: str, day: str, *, inclusive=True) -> int:
        return sum(
            entry["amount"] for transaction in self.state["transactions"]
            if transaction["date"] < day or (inclusive and transaction["date"] == day)
            for entry in transaction["entries"] if entry["accountId"] == account_id
        )

    def _process_month_end(self, actor, month) -> dict:
        if not isinstance(month, str) or not _MONTH.fullmatch(month) or month > self.day[:7]:
            raise BankError("Choose the current month or a past month.", "INVALID_MONTH")
        processed_months = self.state["processedMonths"]
        if month in processed_months:
            raise BankError(f"Month-end processing for {month} is already complete.", "MONTH_ALREADY_PROCESSED", 409)
        if any(processed > month for processed in processed_months):
            raise BankError("Process periods in chronological order.", "MONTH_OUT_OF_ORDER", 409)
        year, month_number = map(int, month.split("-"))
        effective_date = min(f"{month}-{monthrange(year, month_number)[1]:02d}", self.day)
        statements, adjustments = [], []
        # Stage every account before posting, so a failure leaves all balances and ledgers unchanged.
        for original in self._accounts.values():
            if original.created_on > effective_date:
                continue
            account = type(original)(original.snapshot())
            statement, pending = self._stage_statement(account, month, effective_date)
            statements.append(statement)
            adjustments.extend(pending)
        if not statements:
            raise BankError("No eligible accounts were open during this month.", "NO_ACCOUNTS_FOR_MONTH", 409)
        for account, kind, amount in adjustments:
            self._accounts[account.id] = account
            self._post(actor, kind, _DESCRIPTIONS[kind], [_entry(account, amount)], effective_date=effective_date)
        self.state["monthlyStatements"].extend(statements)
        processed_months.append(month)
        self._audit(actor, "monthEnd", f"Processed {month} and generated {len(statements)} monthly statements")
        return {"message": f"Month-end completed for {month}.", "statements": statements}

    def _stage_statement(self, account, month, effective_date):
        opening = self._balance_through(account.id, f"{month}-01", inclusive=False)
        balance = self._balance_through(account.id, effective_date)
        pending = []

        def stage(kind, amount):
            if kind == "interest":
                account.deposit(amount)
                signed_amount = amount
            else:
                account.withdraw(amount, operation=_SERVICE_FEE)
                signed_amount = -amount
            pending.append((account, kind, signed_amount))

        def statement(*, interest, fee):
            return {
                "id": f"ST-{month}-{account.id}", "accountId": account.id, "month": month,
                "openingBalance": opening, "closingBalance": balance + interest - fee, "interest": interest, "fee": fee,
            }

        result = account.process_month_end(balance=balance, post=stage, generate_statement=statement)
        return result, pending


def seed_bank(now: datetime | str | None = None) -> dict:
    """Create a synthetic ledger by running historical transactions through the commands."""
    now = _clock(now)
    users = [
        {
            "id": user_id, "name": name, "email": email, "role": role,
            "passwordHash": _credential_record(password), "pinHash": _credential_record(pin),
        }
        for user_id, name, email, role, password, pin in _DEMO_USERS
    ]
    ayesha, omar = users[0]["id"], users[1]["id"]
    savings, current, fixed, recipient = "10003482", "10007061", "10009123", "10005619"
    records = (
        (savings, ayesha, "Savings Account", "savings"),
        (current, ayesha, "Current Account", "current"),
        (fixed, ayesha, "Fixed Deposit", "fixed"),
        (recipient, omar, "Savings Account", "savings"),
    )
    created_on = _day_of(now - timedelta(days=45))
    maturity = _day_of(now + timedelta(days=45))
    state = {
        "users": users,
        "accounts": [
            {
                "id": account_id, "ownerId": owner, "name": name, "type": account_type, "balance": 0,
                "createdOn": created_on, "dailySpent": {}, "maturesOn": maturity if account_type == "fixed" else None,
            }
            for account_id, owner, name, account_type in records
        ],
        "transactions": [], "notifications": [], "monthlyStatements": [], "processedMonths": [], "audit": [],
        "accountSequence": 10_009_123, "transactionSequence": 100_000, "auditSequence": 100_000,
    }
    activity = (
        (45, 0, ayesha, "deposit", savings, None, 960_420, "Savings opening deposit"),
        (45, 0, ayesha, "deposit", current, None, 386_898, "Current opening deposit"),
        (45, 0, ayesha, "deposit", fixed, None, 750_000, "Fixed deposit funding"),
        (45, 0, omar, "deposit", recipient, None, 202_500, "Savings opening deposit"),
        (7, 0, ayesha, "deposit", savings, None, 320_000, "Salary deposit"),
        (6, 0, ayesha, "withdraw", savings, None, 8_000, "Bookshop purchase"),
        (5, 0, ayesha, "transfer", savings, current, 32_500, "Transfer to Current Account"),
        (4, 1, ayesha, "withdraw", current, None, 125_000, "Monthly rent"),
        (4, 0, ayesha, "withdraw", savings, None, 4_995, "Grocery shopping"),
        (3, 0, ayesha, "deposit", current, None, 245_000, "Freelance payment"),
        (2, 1, ayesha, "withdraw", current, None, 1_499, "Spotify subscription"),
        (2, 0, ayesha, "deposit", savings, None, 15_075, "Cash deposit"),
        (1, 4, ayesha, "withdraw", current, None, 1_850, "Coffee shop"),
        (1, 2, ayesha, "transfer", current, recipient, 15_000, "Transfer to Omar Malik"),
        (1, 0, ayesha, "withdraw", current, None, 31_999, "ATM withdrawal"),
    )
    for days, hours, actor_id, kind, source_id, destination_id, amount, description in activity:
        bank = Bank(state, now - timedelta(days=days, hours=hours))
        source = bank._account(source_id)
        destination = bank._account(destination_id) if destination_id else None
        bank._execute(bank._user(actor_id), kind, bank._command(kind, source, destination, amount), description)
    return state
