# Agent Gatekeeper - AI Coding Agent Prompts & Development Log

**Student Name:** Nikhil Bapu Bhosale  
**Enrolment Number:** PGD202567167  
**Institution:** Shoolini University  
**Tool Used:** Google Antigravity (Agentic AI IDE)  
**Date:** 19 November 2026  
**Target Organization:** Amazon India (Online Store - Digit 7)

---

## 1. Summary of AI Interaction

This project was built using **Google Antigravity** as an agentic AI pair programmer to design, implement, and verify a secure API gatekeeper for AI shopping agents interacting with Amazon India.

---

## 2. Step-by-Step Prompt Log

### Prompt 1: Context & Rule Architecture
> **User Prompt:**  
> "My enrolment number is PGD202567167. The last digit is 7, which corresponds to an online store. I have chosen Amazon India. I need a policy gatekeeper that handles four customer actions: `view_order`, `place_order`, `return`, and `refund`. Draft 8 to 9 specific rules with rule numbers returning ALLOW, ASK CUSTOMER, or BLOCK. Ensure revoked agents are blocked first to solve the Wells Fargo revocation liability problem, and include a clear justification for a Rs. 5,000 spending threshold."

**Agent Response:**  
- Drafted rules R1 through R9.
- Established strict priority: R1 (Revoked agent) -> R2 (Unknown agent) -> R3 (Cross-customer mismatch) -> Action rules R4 to R8 -> R9 (Fallback default block).
- Provided business justification for the ₹5,000 threshold: covers daily grocery and essential items while preventing high-ticket accidental purchases like electronics that are costly and complex to reverse.

---

### Prompt 2: Prototype Implementation
> **User Prompt:**  
> "Implement the complete Python prototype for the gatekeeper. Structure it into:  
> 1. `gatekeeper.py`: SQLite audit log, agent registration, timestamped revocation, and the rule engine. Display my enrolment number PGD202567167.  
> 2. `app.py`: A clean Flask web dashboard displaying my enrolment number, forms to register an agent and test requests, a table of active agents with Revoke buttons, and a live audit log table.  
> 3. `test_cases.py`: Automated test harness executing 6 test cases printing an Expected vs Actual comparison table."

**Agent Response:**  
- Created SQLite database schema with `agents` (agent, customer, registered_at, revoked_at) and `audit` (id, ts, customer, agent, action, amount, decision, rule, reason).
- Implemented `register()`, `revoke()`, and `decide()` functions in `gatekeeper.py`.
- Built Flask web application in `app.py` rendering server-side HTML with interactive registration, request submission, and revocation controls.
- Wrote `test_cases.py` setting up sample data and verifying cases 1 through 6.

---

### Prompt 3: Environment Setup & Test Execution
> **User Prompt:**  
> "Run test_cases.py, ensure all tests pass, and verify Flask runs correctly."

**Agent Response:**  
- Installed Flask in the Python 3.12 environment.
- Executed `python test_cases.py`, achieving 6/6 PASS results across all standard and edge scenarios.
- Verified database persistence in `agentgate.db`.

---

## 3. What I Checked and Changed Personally

To ensure full ownership and understanding of the code, I manually verified and customized several critical aspects:

1. **Explicit R9 Default Rule:**  
   Originally, unmatched actions were simply blocked without a designated rule number. I modified the decision logic in `gatekeeper.py` to assign **R9** explicitly (`BLOCK, R9, "Action not covered by any rule"`). This ensures strict audit traceability for compliance.

2. **Custom Test Case 6 (Cross-Customer Impersonation):**  
   I designed test case 6 to simulate a malicious or misconfigured agent (`RivalBot`, registered to customer Asha) attempting to issue an ₹800 refund on customer Nikk's account. This verifies rule **R3** (`BLOCK, R3`), preventing multi-tenant data leakage or unauthorized account manipulation.

3. **Wells Fargo Compliance Validation:**  
   I verified that `revoke()` updates the `revoked_at` column with `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`. This provides the customer with an immutable audit record proving exactly when agent authority was terminated, directly answering the requirement outlined in American Banker (Nov 2026).

