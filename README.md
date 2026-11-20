# Agent Gatekeeper – Amazon India (Online Store)

**Student Name:** Nikhil Bapu Bhosale  
**Enrolment Number:** PGD202567167  
**Institution:** Shoolini University  
**Specialization:** Online Store Gatekeeper (Enrolment ends in 7)  
**Target Platform:** Amazon India  
**Development Tool:** Google Antigravity (Agentic AI IDE)

---

## 📌 Project Overview

As consumer AI agents (such as Perplexity Comet, ChatGPT Operator, and custom shopping bots) begin autonomously interacting with e-commerce platforms on behalf of customers, retailers face significant security, fraud, and liability challenges.

This repository implements **Agent Gatekeeper**, a lightweight rule-based authorization middleware and audit engine designed for **Amazon India**. When an external agent submits a request (`customer`, `agent`, `action`, `amount`), the gatekeeper returns one of three decisions:
- **`ALLOW`** (with rule ID)
- **`ASK CUSTOMER`** (with rule ID)
- **`BLOCK`** (with rule ID)

It also provides:
1. **Agent lifecycle management**: Registration and revocation with exact timestamping to provide proof of cancellation (answering the Wells Fargo November 2026 legal requirement).
2. **Deterministic rule evaluation (R1 – R9)** with strict priority ordering.
3. **Persistent SQLite audit logging**: Recording every single evaluation with timestamp, parameters, decision, and rationale.
4. **Flask web dashboard**: Visual interface displaying enrolment number `PGD202567167`, interactive registration/request forms, active agents table with one-click revocation, and real-time audit logs.

---

## 🛡️ Rule Architecture (R1 – R9)

Evaluated in strict hierarchical order:

| Rule | Condition / Scenario | Decision | Rationale |
| :--- | :--- | :--- | :--- |
| **R1** | Agent is revoked (`revoked_at` is set) | **`BLOCK`** | Customer revoked consent; Amazon must honor immediately and maintain timestamp as legal proof. |
| **R2** | Agent is unknown / not registered | **`BLOCK`** | Zero-trust security: untrusted entity Amazon has never authorized. |
| **R3** | Agent registered to a different customer | **`BLOCK`** | Cross-account segregation: prevent agent from manipulating another customer's account. |
| **R4** | `view_order` (read-only) | **`ALLOW`** | Zero financial or inventory impact (analogous to JPMorgan permitting balance inquiries). |
| **R5** | `place_order` where amount <= ₹4,000 | **`ALLOW`** | Routine daily grocery/essential purchases; low risk and easily manageable via standard returns. |
| **R6** | `place_order` where amount > ₹4,000 | **`ASK CUSTOMER`** | High-ticket purchases (smartphones, electronics) carry substantial financial and restocking risk. |
| **R7** | `return` item | **`ASK CUSTOMER`** | Alters logistics, shipping, and inventory state; requires explicit customer confirmation. |
| **R8** | `refund` (any amount) | **`ASK CUSTOMER`** | Transfers money out of Amazon; highest fraud vulnerability requiring customer step-up verification. |
| **R9** | Any unmapped action | **`BLOCK`** | Default-deny policy: reject any unrecognized or unclassified action. |

---

## 🧪 Verification & Test Suite

The automated test suite in `test_cases.py` validates the six core evaluation scenarios:

| # | Test Scenario | Expected | Actual | Result |
| :-: | :--- | :--- | :--- | :-: |
| 1 | Known agent (`ShopBot`) views an order | `ALLOW, R4` | `ALLOW, R4` | **PASS** |
| 2 | Unknown agent (`GhostBot`) places ₹500 order | `BLOCK, R2` | `BLOCK, R2` | **PASS** |
| 3 | Known agent places ₹12,000 order (> ₹5,000 limit) | `ASK CUSTOMER, R6` | `ASK CUSTOMER, R6` | **PASS** |
| 4 | Known agent places ₹1,500 order (<= ₹5,000 limit) | `ALLOW, R5` | `ALLOW, R5` | **PASS** |
| 5 | Revoked agent (`OldBot`) attempts to view order | `BLOCK, R1` | `BLOCK, R1` | **PASS** |
| 6 | `RivalBot` (registered to Asha) asks for ₹800 refund on Nikk's account | `BLOCK, R3` | `BLOCK, R3` | **PASS** |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Flask (`pip install flask`)
- ReportLab (`pip install reportlab`, for PDF compilation)

### 2. Run the Automated Tests
```bash
python test_cases.py
```

### 3. Launch the Web Interface
```bash
python app.py
```
Open your browser to `http://127.0.0.1:5000` to interact with the gatekeeper dashboard.

### 4. Regenerate the Report PDF
To regenerate `PGD202567167_AgentGate_Report.pdf` with your specific GitHub link:
```bash
python generate_report.py "https://github.com/your-username/AgentGate"
```

---

## 📂 Repository Contents

```text
├── app.py                            # Flask web application dashboard
├── gatekeeper.py                     # Core logic, database schema, and rule engine
├── test_cases.py                     # Automated 6-scenario verification test harness
├── generate_report.py                # Script compiling the formal 2-page academic report
├── PGD202567167_AgentGate_Report.pdf # Final compiled 2-page report PDF
├── PROMPTS.md                        # Documentation of AI agent prompts and student modifications
├── VIDEO_SCRIPT.md                   # 2-minute spoken video script with screen recording cues
├── package_submission.py             # Packaging utility creating the final ZIP bundle
└── README.md                         # Project documentation and guide
```

---

## 📜 Academic Integrity & Attribution
Developed with guidance from **Google Antigravity**. All rule adaptations, edge case design (R9, Test Case 6), and policy rationales were reviewed, verified, and configured by **Nikhil Bapu Bhosale**.

