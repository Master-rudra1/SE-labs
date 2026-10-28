# Lab 5: Static Code Analysis — Scholarship Disbursement Ledger

This folder contains the deliverables for **Lab 5: Static Code Analysis** for the Scholarship Disbursement Ledger system.

## Deliverables Summary

1. **`scholarship_disbursement.py`**: Cleaned, secure, PEP 8-compliant source code with:
   - **Pylint Score**: `10.00 / 10` (exceeds the required `> 9.5` threshold).
   - **Bandit**: `0` issues (all CWE-89, CWE-78, and CWE-703 issues resolved).
   - **Flake8**: `0` violations (all PEP 8 and line-length rules satisfied).
2. **`issues.md`**: Completed issue documentation table detailing all identified issues, categories, line numbers, descriptions, and resolution methods.
3. **`reflection.md`**: Comprehensive reflection report answering the static code analysis questions.
4. **Analysis Reports (Before and After)**:
   - `pylint_report.txt` & `pylint_report_before.txt`
   - `bandit_report.txt` & `bandit_report_before.txt`
   - `flake8_report.txt` & `flake8_report_before.txt`
   - `reports/before/` and `reports/after/` directories containing full report logs.

## How to Run

### 1. Execute the Program
```bash
python scholarship_disbursement.py
```

### 2. Run Static Analysis Tools
```bash
pylint scholarship_disbursement.py
bandit -r scholarship_disbursement.py
flake8 scholarship_disbursement.py
```
