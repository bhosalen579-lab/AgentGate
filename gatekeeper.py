"""Agent Gatekeeper - core logic (Amazon India, online store). Enrolment: PGD202567167"""
import sqlite3
from datetime import datetime

ENROLMENT = "PGD202567167"
COMPANY = "Amazon India"
LIMIT = 5000          # Rs. limit for place_order without asking the customer
DB = "agentgate.db"
ACTIONS = ["view_order", "place_order", "return", "refund"]


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS agents(
            agent TEXT PRIMARY KEY, customer TEXT, registered_at TEXT, revoked_at TEXT);
        CREATE TABLE IF NOT EXISTS audit(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, customer TEXT, agent TEXT,
            action TEXT, amount REAL, decision TEXT, rule TEXT, reason TEXT);
        """)


def register(agent, customer):
    with db() as c:
        c.execute("INSERT OR REPLACE INTO agents VALUES (?,?,?,NULL)", (agent, customer, now()))


def revoke(agent):
    """Save the date and time of revocation (the Wells Fargo problem)."""
    with db() as c:
        c.execute("UPDATE agents SET revoked_at=? WHERE agent=? AND revoked_at IS NULL", (now(), agent))


def decide(customer, agent, action, amount=0):
    with db() as c:
        a = c.execute("SELECT * FROM agents WHERE agent=?", (agent,)).fetchone()
    # Order matters: R1 first, so a revoked agent is blocked before anything else
    if a and a["revoked_at"]:
        d = ("BLOCK", "R1", f"Agent was revoked on {a['revoked_at']}")
    elif not a:
        d = ("BLOCK", "R2", "Unknown agent")
    elif a["customer"] != customer:
        d = ("BLOCK", "R3", "Agent is not registered for this customer")
    elif action == "view_order":
        d = ("ALLOW", "R4", "Read-only action")
    elif action == "place_order" and amount <= LIMIT:
        d = ("ALLOW", "R5", f"Order within Rs.{LIMIT} limit")
    elif action == "place_order":
        d = ("ASK CUSTOMER", "R6", f"Order above Rs.{LIMIT} limit")
    elif action == "return":
        d = ("ASK CUSTOMER", "R7", "Returns need customer confirmation")
    elif action == "refund":
        d = ("ASK CUSTOMER", "R8", "Refunds need customer confirmation")
    else:
        d = ("BLOCK", "R9", "Action not covered by any rule")
    with db() as c:
        c.execute("INSERT INTO audit(ts,customer,agent,action,amount,decision,rule,reason) VALUES (?,?,?,?,?,?,?,?)",
                  (now(), customer, agent, action, amount, *d))
    return d
