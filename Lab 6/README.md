# Lab 6: Code and Branch Coverage Analysis

**Student Name:** Rudra Dhadhal  
**SRN:** PES1UG24CS146  
**Course:** Software Engineering (UE24CS342AA2)  
**Assigned Repository:** [SETAPESU26/L6_L7_20_food_delivery](https://github.com/SETAPESU26/L6_L7_20_food_delivery)  
**Module Under Test:** `food_delivery.py`

---

## 1. Objectives

- Differentiate between **code (line/statement) coverage** and **branch coverage**.
- Use Python's `coverage` tool to measure, analyze, and improve test suite completeness.
- Identify untested decision paths, dead code, and logical edge cases.
- Achieve >= 90% coverage for both code coverage and branch coverage (achieved **100%** on both).

---

## 2. Deliverables Summary

| Deliverable | Description | File Path |
|---|---|---|
| **Code Coverage Test Cases** | Targeted test cases exercising every statement | `CodeCoverageTest_food_delivery.py` / `CodeCoverageTest_PES1UG24CS146_food_delivery.py` |
| **Branch Coverage Test Cases** | Comprehensive test cases covering all decision branches & boundaries | `BranchCoverageTest_food_delivery.py` / `BranchCoverageTest_PES1UG24CS146_food_delivery.py` |
| **Code Coverage Screenshot** | Terminal output screenshot showing 100% statement coverage | `code_coverage_analysis.png` |
| **Branch Coverage Screenshot** | Terminal output screenshot showing 100% branch coverage (0 missing branches) | `branch_coverage_analysis.png` |
| **Initial / Extended Tests** | Starter test file extended to cover application requirements | `test_food_delivery.py` |
| **Text Reports** | Coverage analysis reports generated via `coverage report -m` | `code_coverage_report.txt`, `branch_coverage_report.txt` |

---

## 3. Code Coverage vs. Branch Coverage Concepts

| Type | Definition | Focus |
|---|---|---|
| **Line Coverage** | Percentage of executable statements visited during testing. | *Did the execution flow pass through this line of code at least once?* |
| **Branch Coverage** | Percentage of decision branches (`if`, `elif`, `else`, boolean short-circuits) evaluated to both `True` and `False`. | *Did every control structure and conditional path evaluate to both possible outcomes?* |
| **Path Coverage** | Measures execution of every unique end-to-end combination of paths. | Tests all possible combinations of decision branches. |
| **Function Coverage** | Measures percentage of declared functions invoked during testing. | Verifies all module functions are called. |

---

## 4. Phase 1: Code Coverage Analysis

### Test Design
The test suite in `CodeCoverageTest_food_delivery.py` is structured into three test classes targeting the functions in `food_delivery.py`:
- `TestDeliveryChargeCodeCoverage`: Validates distance thresholds, order value discount rules, and rain surcharge execution.
- `TestApplyCouponCodeCoverage`: Tests valid coupons, invalid codes, non-first order restrictions for `WELCOME`, and minimum spend limits.
- `TestEstimatedTimeCodeCoverage`: Tests travel time computation under combined peak hour and busy kitchen conditions.

### Terminal Output
```
PS C:\Users\rudra\SE-labs\Lab 6> coverage run -m pytest CodeCoverageTest_food_delivery.py
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\rudra\SE-labs\Lab 6
plugins: anyio-4.14.2
collected 11 items

CodeCoverageTest_food_delivery.py ...........                            [100%]

======================== 11 passed in 0.05s ========================

PS C:\Users\rudra\SE-labs\Lab 6> coverage report -m
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
CodeCoverageTest_food_delivery.py      30      0   100%
food_delivery.py                       33      0   100%
-----------------------------------------------------------------
TOTAL                                  63      0   100%
```

![Code Coverage Terminal Output](code_coverage_analysis.png)

---

## 5. How to Reproduce

### 1. Install Dependencies
```bash
pip install coverage pytest
```

### 2. Run Code Coverage
```bash
coverage erase
coverage run -m pytest CodeCoverageTest_food_delivery.py
coverage report -m
```

### 3. Run Branch Coverage
```bash
coverage erase
coverage run --branch -m pytest BranchCoverageTest_food_delivery.py
coverage report -m
```
