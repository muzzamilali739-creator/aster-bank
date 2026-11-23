# Aster Bank

A desktop-first banking simulation for an object-oriented programming project. Python implements the banking rules, design patterns, and HTTP API. SQLite stores the local ledger and banking sessions. The browser interface uses HTML, CSS, and vanilla JavaScript.

## Run locally

Requires Python 3.10 or newer. The project uses the Python standard library. Extract the source archive and open a terminal in the project directory.

On macOS or Linux, run the server from the project directory.

```sh
python3 server.py
```

On Windows, use the Python launcher.

```powershell
py server.py
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Keep the terminal open to see simulated SMS and email alerts. Press `Ctrl+C` to stop the server.

The first visit opens Ayesha’s sample customer session. Open **Demo Lab** to run the project scenarios. Use the sample profiles to demonstrate the teller and administrator views, or sign out and register a customer.

| Sample profile | Email | PIN |
| --- | --- | --- |
| Ayesha Khan, customer | `ayesha@aster.demo` | `123456` |
| Omar Malik, customer | `omar@aster.demo` | `234567` |
| Hamza Ali, bank teller | `teller@aster.demo` | `112233` |
| Sara Ahmed, bank admin | `admin@aster.demo` | `654321` |

The shared sample password is `AsterDemo1!`. These are synthetic profiles with simulated USD balances.

## Run the tests

```sh
python3 -m unittest discover -s tests
```

On Windows, use `py -m unittest discover -s tests`.

## Diagrams and walkthrough

- [Use case diagram](docs/use-case.svg) with four actors, 13 use cases, and the UML «include» and «extend» relationships. Drawn as a digital pen-style vector sketch.
- [Transfer Funds sequence diagram](docs/transfer-sequence.svg) showing the Python Proxy and Command calls, Observer delivery, and SQLite commit.
- [Project guide](docs/project-guide.md) with account rules, class relationships, pattern references, and a five-part demo walkthrough.

## Source map

| File | Purpose |
| --- | --- |
| [server.py](server.py) | Entry point for the local desktop site |
| [aster_bank/bank.py](aster_bank/bank.py) | Account types, validated balance operations, transaction commands, Observer, protection Proxy, audit history, and month-end processing |
| [aster_bank/server.py](aster_bank/server.py) | HTTP API, authentication, persistence, and static file serving |
| [drizzle/0000_initial.sql](drizzle/0000_initial.sql) | SQLite workspace schema |
| [dist/client/index.html](dist/client/index.html) | Browser shell and accessible navigation |
| [dist/client/styles.css](dist/client/styles.css) | Desktop and responsive layouts |
| [dist/client/app.mjs](dist/client/app.mjs) | Dashboard, workflows, statements, alerts, and Demo Lab |

The server creates `.data/bank.sqlite` on first run and reuses it across restarts. Banking roles and PIN checks are enforced on the server.

The assignment mentions a separate **COMMON REQUIREMENTS** list that was absent from the supplied brief. The project guide maps the requirements that were provided.
