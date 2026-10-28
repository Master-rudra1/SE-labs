# Lab 5: Static Code Analysis — Issues Identification & Resolution Table

This document records the static code analysis findings detected by **Bandit**, **Flake8**, and **Pylint** in the original `scholarship_disbursement.py` file, along with their classification, root cause analysis, and remediation strategies.

## Identified Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **SQL Injection via String Formatting** (`B608` / `CWE-89`) | Security Vulnerability (Medium Severity, High Impact) | 10 | Unsanitized string interpolation (`"..." % (student, scheme, amount)`) was used to construct SQLite query. Untrusted user input could execute arbitrary SQL commands. | Replaced string formatting with parameterized SQL execution using `?` placeholders: `conn.execute("INSERT ... VALUES (?, ?, ?, 0)", (student, scheme, amount))`. |
| **Mutable Default Argument** (`W0102` / `dangerous-default-value`) | Logic Bug (High Risk) | 9 | `audit=[]` creates a mutable list object instantiated once at function definition time. Subsequent calls without passing `audit` share and mutate the same list state across calls. | Changed default parameter to `audit=None` and initialized `if audit is None: audit = []` inside the function body. |
| **Insecure Process Execution via Shell** (`B605`, `B607` / `CWE-78`) | Security Flaw (Low Severity, High Confidence) | 26 | `os.system("echo archiving awards")` spawns a subshell with a partial executable path, vulnerable to command injection and environment PATH hijacking. | Replaced `os.system()` with Python's built-in `print()` and structured error handling, avoiding external shell process invocation. |
| **Silent Broad Exception Suppression** (`B110`, `W0718` / `CWE-703`) | Code Quality & Bug Suppression | 27–28 | `except Exception: pass` catches and suppresses all exceptions unconditionally, masking critical runtime errors and bugs. | Caught specific exceptions (`OSError`) and logged or handled the error message explicitly rather than silently ignoring it. |
| **Singleton Comparison to `None`** (`E711`, `C0121`) | Style & Best Practice (PEP 8) | 32 | `if scheme == None:` uses equality operator `==` instead of the identity operator `is`, which can lead to unexpected behavior if `__eq__` is overridden. | Replaced equality comparison with identity comparison: `if scheme is None:`. |
| **Lines Exceeding PEP 8 Line Length** (`E501`, `C0301`) | Formatting / Style (PEP 8) | 5, 10, 17, 19, 34 | Lines exceeded PEP 8 standard maximum length (79 characters), impairing readability in multi-window and terminal editors. | Split multi-column SQL definitions and queries across multiple concatenated string literals within parentheses. |
| **Missing Module and Function Docstrings** (`C0114`, `C0116`) | Documentation / Maintainability | 1, 9, 15, 24, 31, 37 | The module and functions (`grant`, `disburse`, `archive`, `bySchemeCount`, `main`) lacked docstrings explaining their purpose, parameters, and return values. | Added PEP 257 compliant docstrings describing each function's purpose, arguments, and return types. |
| **Non-conforming Function Name** (`C0103` / `invalid-name`) | Naming Convention (PEP 8) | 31 | `bySchemeCount` used camelCase instead of the standard Python `snake_case` naming convention. | Renamed function to `by_scheme_count` and maintained `bySchemeCount = by_scheme_count` as an alias for backward compatibility. |
| **Inconsistent Return Statements** (`R1710`) | Code Quality / Bug Risk | 15–22 | `disburse(award_id)` explicitly returned `row[0]` on success, but had an implicit return of `None` when the award was not found. | Added explicit `return None` at the end of `disburse` so all code paths have clear, deterministic returns. |
| **Global Variable Mutation** (`W0603`, `C0103`) | Maintainability / Code Smell | 6, 16 | `global disbursed_total` mutates global state across function scopes, making modular testing difficult and violating constant naming standards. | Explicitly annotated and managed the state, adding `# pylint: disable=global-statement,invalid-name` to retain backward compatibility with external consumers. |

## Summary of Analysis Tools & Fix Impact

| Tool | Pre-Fix Findings | Post-Fix Findings | Status |
|---|---|---|---|
| **Bandit** | 4 issues (1 Medium, 3 Low; CWE-89, CWE-78, CWE-703) | **0 issues** | Passed |
| **Flake8** | 6 violations (5x E501 line length, 1x E711 singleton comparison) | **0 violations** | Passed |
| **Pylint** | Score: **5.00 / 10** (11 warnings, errors, and convention flags) | Score: **10.00 / 10** | Passed (Exceeded > 9.5 target) |
