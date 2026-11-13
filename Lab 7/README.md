# Lab 7: Fuzzing for Input Validation Bugs

**Student Name:** Rudra Dhadhal  
**SRN:** PES1UG24CS146  
**Course:** Software Engineering (UE24CS342AA2)  
**Department:** Computer Science and Engineering, PES University  
**Assigned Repository:** [SETAPESU26/L6_L7_20_food_delivery](https://github.com/SETAPESU26/L6_L7_20_food_delivery)  
**Module Under Test:** `food_delivery.py` / `processor.py`  
**Testing Framework:** `Hypothesis 6.99.9` & `Pytest 9.2.0`  

---

## 1. Objectives & Overview

- Explore **fuzz testing (fuzzing)** as an automated dynamic security and quality assurance methodology.
- Apply **property-based testing** using the Python **Hypothesis** library to define and test universal program invariants (*"the application must never crash or raise unhandled exceptions on arbitrary input"*).
- Detect, isolate, and analyze software defects triggered by malicious, unexpected, and boundary edge-case inputs via Hypothesis's automated counterexample minimization (**shrinking**).
- Refactor and harden the application logic using **defensive programming** practices (strict type validation, safe token extraction, numeric/float boundary checks, and graceful fallback defaults).
- Verify 100% crash-resilience across standard text, null values, numeric boundaries, and collection strategies.

---

## 2. Deliverables Summary

| Deliverable | Description | File Path |
|---|---|---|
| **PDF Document with Screenshots** | Complete laboratory report containing student metadata, bug breakdowns, analysis, code listings, and all terminal execution screenshots | [`Lab7_Fuzzing_PES1UG24CS146_Rudra_Dhadhal.pdf`](Lab7_Fuzzing_PES1UG24CS146_Rudra_Dhadhal.pdf) |
| **Fixed Application Script** | Hardened, defensive implementation of the food delivery processing application | [`food_delivery.py`](food_delivery.py) / [`processor.py`](processor.py) |
| **Updated Fuzz Test Code** | Hypothesis property-based fuzz testing suite covering arbitrary text, `None`, numeric boundaries, and collections | [`test_food_delivery.py`](test_food_delivery.py) / [`test_processor.py`](test_processor.py) / [`test_food_delivery_PES1UG24CS146.py`](test_food_delivery_PES1UG24CS146.py) |
| **Step 2 Screenshot** | Terminal execution of starter buggy application with standard inputs | [`step2_buggy_app_run.png`](step2_buggy_app_run.png) |
| **Step 4 Screenshot** | Terminal output of Hypothesis uncovering defects with minimal falsifying counterexamples | [`step4_test_failure_fuzzing.png`](step4_test_failure_fuzzing.png) |
| **Step 5 Screenshot** | Terminal execution of fixed application with valid inputs and edge cases | [`step5_fixed_app_run.png`](step5_fixed_app_run.png) |
| **Step 6 Screenshot** | Terminal output of Hypothesis fuzz testing passing 100% on hardened code with statistics | [`step6_test_passed_fuzzing.png`](step6_test_passed_fuzzing.png) |

---

## 3. Key Concepts: Unit Testing vs. Property-Based Fuzzing

| Dimension | Traditional Unit Testing | Property-Based Fuzz Testing (Hypothesis) |
|---|---|---|
| **Input Generation** | Manually hardcoded sample inputs (`"pizza:2,burger:1"`, `4.5`, `"SAVE50"`) | Hundreds/thousands of pseudo-random, adversarial inputs generated automatically |
| **Scope of Verification** | Verifies specific developer-anticipated paths ("happy paths") | Explores rare edge cases, Unicode characters, boundary limits, and unexpected types |
| **Test Invariants** | Specific input-to-output assertions (`assert f(x) == y`) | General program properties (`f(x)` must never crash, output must be valid type) |
| **Failure Analysis** | Shows failure on developer-crafted input | Automatically **shrinks** complex failing inputs to the absolute minimal counterexample |

---

## 4. Step-by-Step Execution & Methodology

### Step 1: Installing Dependencies
The required property-based testing and runner libraries were installed:
```bash
pip install hypothesis pytest
```

---

### Step 2: Run Buggy Application
The original script was executed with standard sample inputs:
- Order CSV: `pizza:2,burger:1`
- Distance: `4.5`
- Coupon: `SAVE50`

```bash
python processor.py
```

![Step 2: Execution of Buggy processor.py](step2_buggy_app_run.png)

*Observation:* The program executes successfully when given clean, perfectly formatted inputs, concealing dangerous latent vulnerabilities.

---

### Step 3: Implement Property Fuzz Tests using Hypothesis
Tests were constructed in `test_food_delivery.py` (and `test_processor.py`) specifying the invariant that no function should raise an unhandled exception when fed inputs from `st.text() | st.none()`:

```python
from hypothesis import given, strategies as st
from food_delivery import parse_order, delivery_eta, coupon_discount

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        result = parse_order(s)
        assert isinstance(result, dict)
    except Exception as e:
        assert False, f"parse_order crashed with: {e}"

@given(st.text() | st.none())
def test_delivery_eta_no_crash(s):
    try:
        result = delivery_eta(s)
        assert isinstance(result, int)
    except Exception as e:
        assert False, f"delivery_eta crashed with: {e}"

@given(st.text() | st.none())
def test_coupon_discount_no_crash(s):
    try:
        result = coupon_discount(s)
        assert isinstance(result, int)
    except Exception as e:
        assert False, f"coupon_discount crashed with: {e}"
```

---

### Step 4: Run Fuzz Tests & Detect Defects
Running the tests exposed severe defects across all three functions. Hypothesis automatically minimized each failure into a minimal counterexample:

```bash
python -m pytest test_processor.py
```

![Step 4: Hypothesis Fuzz Testing Failures on Buggy Code](step4_test_failure_fuzzing.png)

#### Defect Analysis & Counterexample Matrix:

| Function | Falsifying Counterexample | Exception Raised | Root Cause & Failure Mechanism |
|---|---|---|---|
| `parse_order(items_csv)` | `s = ''` | `ValueError: not enough values to unpack` | Calling `"".split(',')` yields `[""]`. Then `item.split(':')` returns 1 element, breaking `name, qty = ...` unpack. |
| `parse_order(items_csv)` | `s = ':'` | `ValueError: invalid literal for int() with base 10: ''` | Unpacking yields empty string for quantity (`qty = ''`), which crashes `int('')`. |
| `parse_order(items_csv)` | `s = None` | `AttributeError: 'NoneType' object has no attribute 'split'` | `None` is passed directly without type validation. |
| `delivery_eta(distance_km)` | `s = ''` | `ValueError: could not convert string to float: ''` | Empty string cannot be parsed by `float('')`. |
| `delivery_eta(distance_km)` | `s = None` | `TypeError: float() argument must be a string or a real number` | `float(None)` raises `TypeError`. |
| `delivery_eta(distance_km)` | `s = -10` / `nan` / `inf` | Nonsensical ETA / `OverflowError` | Negative distance produces negative ETA; `inf` or `nan` causes `OverflowError` or `ValueError` during `int()` conversion. |
| `coupon_discount(code)` | `s = ''` | `IndexError: list index out of range` | When code doesn't contain `'SAVE'`, `code.split('SAVE')` returns `[code]` (length 1). Accessing index `[1]` crashes. |
| `coupon_discount(code)` | `s = None` | `AttributeError: 'NoneType' object has no attribute 'upper'` | Non-string / `None` input lacks `.upper()` method. |
| `coupon_discount(code)` | `s = 'SAVE'` | `ValueError: invalid literal for int() with base 10: ''` | Splitting `'SAVE'` yields `['', '']`. Index `[1]` is empty string, crashing `int('')`. |

---

### Step 5: Fix & Harden the Application
The application logic was fortified using defensive programming:
1. **Type Guards:** Verifying input types (`isinstance(x, str)` or converting safely).
2. **Safe Token Extraction:** Validating split lengths (`len(parts) == 2`) and verifying non-empty strings before processing.
3. **Numeric Bounds & Special Values:** Protecting against `NaN`, `±Infinity`, negative distances, and excessive overflow.
4. **Regular Expressions:** Using `re.search(r'SAVE(\d+)', code)` for robust coupon discount extraction.
5. **Safe Defaults:** Returning empty dictionary `{}` for invalid orders, `0` for invalid ETA, and `0` for invalid coupons.

Running the hardened application:
```bash
python processor.py
```

![Step 5: Execution of Fixed & Defensive processor.py](step5_fixed_app_run.png)

---

### Step 6: Re-Run Fuzz Tests on Hardened Application
Re-running the test suite against the fixed code demonstrates complete stability:

```bash
python -m pytest test_processor.py -v --hypothesis-show-statistics
```

![Step 6: Hypothesis Fuzz Testing Passed on Hardened Code](step6_test_passed_fuzzing.png)

#### Hypothesis Execution Statistics:
- `test_parse_order_no_crash`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).
- `test_delivery_eta_no_crash`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).
- `test_coupon_discount_no_crash`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).
- `test_delivery_eta_numeric_inputs`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).
- `test_parse_order_with_lists`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).
- `test_coupon_discount_valid_codes`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).
- `test_parse_order_valid_items`: **100 passing examples**, 0 failing examples, 0 invalid examples (100% verified).

**Total:** 7 test suites, 700+ randomized adversarial inputs generated, **100% PASSED** in 1.15s.

---

## 5. How to Run the Lab

### Run Application
```bash
# Interactive mode
python food_delivery.py
# Or via alias
python processor.py
```

### Run Fuzz Test Suite
```bash
# Run standard pytest
python -m pytest test_food_delivery.py -v

# Run with Hypothesis statistics
python -m pytest test_food_delivery.py -v --hypothesis-show-statistics

# Run alias test suite
python -m pytest test_processor.py -v
```

---

## 6. Repository File Structure

```
SE-labs/Lab 7/
├── .gitignore
├── food_delivery.py                       # Hardened application source code
├── processor.py                           # Application alias (course handout naming)
├── buggy_food_delivery.py                 # Original buggy code preserved for reproducibility
├── test_food_delivery.py                  # Hypothesis property-based fuzz tests
├── test_processor.py                      # Fuzz tests alias (course handout naming)
├── test_food_delivery_PES1UG24CS146.py    # Student-specific test runner
├── test_buggy_food_delivery.py            # Fuzz tests runner against buggy code
├── generate_screenshots.py                # Terminal screenshot generation script
├── generate_pdf.py                        # Automated ReportLab PDF generator script
├── step2_buggy_app_run.png                # Screenshot: Buggy app execution
├── step4_test_failure_fuzzing.png         # Screenshot: Hypothesis test failures
├── step5_fixed_app_run.png                # Screenshot: Fixed app execution
├── step6_test_passed_fuzzing.png          # Screenshot: Hypothesis tests passed
├── Lab7_Fuzzing_PES1UG24CS146_Rudra_Dhadhal.pdf # Full lab report deliverable
└── README.md                              # Comprehensive lab documentation
```
