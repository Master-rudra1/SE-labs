"""
Hypothesis Fuzz Testing Suite for Food Delivery Application.

Course: Software Engineering Lab 7 - Fuzzing for Input Validation Bugs
Student Name: Rudra Dhadhal
SRN: PES1UG24CS146
Course Code: UE24CS342AA2
"""

from hypothesis import given, strategies as st
from food_delivery import parse_order, delivery_eta, coupon_discount


# =====================================================================
# Phase 1: Core Property Fuzz Tests (st.text() | st.none())
# As specified in Lab 7 handout to uncover crashes on malformed inputs
# =====================================================================

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    """Ensure parse_order never crashes on arbitrary text or None."""
    try:
        result = parse_order(s)
        assert isinstance(result, dict)
    except Exception as e:
        assert False, f"parse_order crashed with: {e}"


@given(st.text() | st.none())
def test_delivery_eta_no_crash(s):
    """Ensure delivery_eta never crashes on arbitrary text or None."""
    try:
        result = delivery_eta(s)
        assert isinstance(result, int)
    except Exception as e:
        assert False, f"delivery_eta crashed with: {e}"


@given(st.text() | st.none())
def test_coupon_discount_no_crash(s):
    """Ensure coupon_discount never crashes on arbitrary text or None."""
    try:
        result = coupon_discount(s)
        assert isinstance(result, int)
    except Exception as e:
        assert False, f"coupon_discount crashed with: {e}"


# =====================================================================
# Phase 2: Extended Fuzzing Strategies
# Validating boundary numbers, floats, collections, and arbitrary types
# =====================================================================

@given(st.integers() | st.floats() | st.none())
def test_delivery_eta_numeric_inputs(val):
    """Fuzz delivery_eta with integers, negative numbers, floats, NaN, and Inf."""
    try:
        result = delivery_eta(val)
        assert isinstance(result, int)
        assert result >= 0
    except Exception as e:
        assert False, f"delivery_eta crashed on numeric/special value {val}: {e}"


@given(st.lists(st.text(), max_size=5))
def test_parse_order_with_lists(items):
    """Fuzz parse_order with unexpected list structures."""
    try:
        result = parse_order(items)
        assert isinstance(result, dict)
    except Exception as e:
        assert False, f"parse_order crashed on list input: {e}"


@given(st.integers(min_value=0, max_value=1000))
def test_coupon_discount_valid_codes(discount_amt):
    """Verify valid coupon codes correctly extract the discount amount."""
    code = f"SAVE{discount_amt}"
    result = coupon_discount(code)
    assert result == discount_amt


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=10),
       st.integers(min_value=1, max_value=50))
def test_parse_order_valid_items(item_name, qty):
    """Verify well-formed orders parse accurately."""
    csv_str = f"{item_name}:{qty}"
    result = parse_order(csv_str)
    assert result.get(item_name) == qty
