"""
Test file for food_delivery.py
Initial starter test cases plus additional coverage tests.
"""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# Initial starter test cases from assigned repository:
def test_nearby_small_order():
    assert delivery_charge(2, 200, False) == 20


def test_no_coupon():
    assert apply_coupon(300, None, False) == 300


# Extended test cases to achieve >90% code coverage:
def test_delivery_charge_out_of_range():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(0, 200, False)


def test_delivery_charge_free_delivery():
    assert delivery_charge(5, 500, False) == 0


def test_delivery_charge_medium_distance():
    assert delivery_charge(6, 200, True) == 70


def test_delivery_charge_long_distance():
    assert delivery_charge(10, 200, True) == 90


def test_apply_coupon_invalid():
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(200, "INVALID", True)


def test_apply_coupon_welcome_existing_customer():
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(200, "WELCOME", False)


def test_apply_coupon_below_200():
    assert apply_coupon(150, "SAVE50", True) == 150


def test_apply_coupon_valid_discount():
    assert apply_coupon(250, "SAVE50", True) == 200


def test_estimated_time_busy_peak():
    assert estimated_time(5, True, True) == 65
