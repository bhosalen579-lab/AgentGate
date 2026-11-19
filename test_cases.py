"""Runs the 6 test cases and prints expected vs actual."""
import os
import gatekeeper as g

if os.path.exists(g.DB):
    os.remove(g.DB)
g.init()
g.register("ShopBot", "Nikk")
g.register("OldBot", "Nikk")
g.revoke("OldBot")
g.register("RivalBot", "Asha")

cases = [  # (description, customer, agent, action, amount, expected decision, expected rule)
    ("Known agent, view order",         "Nikk", "ShopBot",  "view_order",  0,     "ALLOW", "R4"),
    ("Unknown agent",                   "Nikk", "GhostBot", "place_order", 500,   "BLOCK", "R2"),
    ("Order above limit (Rs.12000)",    "Nikk", "ShopBot",  "place_order", 12000, "ASK CUSTOMER", "R6"),
    ("Order below limit (Rs.1500)",     "Nikk", "ShopBot",  "place_order", 1500,  "ALLOW", "R5"),
    ("Revoked agent tries to act",      "Nikk", "OldBot",   "view_order",  0,     "BLOCK", "R1"),
    ("Own case: agent of another customer", "Nikk", "RivalBot", "refund",  800,   "BLOCK", "R3"),
]
print(f"{'#':<2} {'Case':<38} {'Expected':<18} {'Actual':<18} Pass")
for i, (desc, cu, ag, ac, am, ed, er) in enumerate(cases, 1):
    d, r, _ = g.decide(cu, ag, ac, am)
    print(f"{i:<2} {desc:<38} {ed+' '+er:<18} {d+' '+r:<18} {'PASS' if (d, r) == (ed, er) else 'FAIL'}")
