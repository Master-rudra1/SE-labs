"""
Code Coverage Test Suite for Food Delivery Application
Author: Rudra Dhadhal (SRN: PES1UG24CS146)
Lab 6: Code and Branch Coverage Analysis

Objective:
This test suite is designed to achieve 100% Code (Line/Statement) Coverage
on `food_delivery.py` (>90% threshold required by rubric). Every executable line
is exercised at least once.
"""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


class TestDeliveryChargeCodeCoverage:
    """Tests designed to execute every line of delivery_charge."""

    def test_delivery_charge_out_of_range_negative(self):
        """Executes line 5 (True condition) and line 6 (raise ValueError)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(0, 250, False)

    def test_delivery_charge_free_delivery_large_order(self):
        """Executes line 7 (True condition) and line 8 (charge = 0)."""
        assert delivery_charge(5, 500, False) == 0

    def test_delivery_charge_short_distance_with_rain(self):
        """Executes line 9 (True condition), line 10 (charge = 20), line 15, 16 (+30), and line 17."""
        assert delivery_charge(2, 200, True) == 50

    def test_delivery_charge_medium_distance_with_rain(self):
        """Executes line 11 (True condition), line 12 (charge = 40), line 15, 16 (+30), and line 17."""
        assert delivery_charge(6, 200, True) == 70

    def test_delivery_charge_long_distance_with_rain(self):
        """Executes line 13, line 14 (charge = 60), line 15, 16 (+30), and line 17."""
        assert delivery_charge(10, 200, True) == 90


class TestApplyCouponCodeCoverage:
    """Tests designed to execute every line of apply_coupon."""

    def test_apply_coupon_none(self):
        """Executes line 21 (True condition) and line 22 (return order_value)."""
        assert apply_coupon(300, None, False) == 300

    def test_apply_coupon_invalid_code(self):
        """Executes line 23 (True condition) and line 24 (raise ValueError)."""
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(300, "DISCOUNT50", False)

    def test_apply_coupon_welcome_existing_customer(self):
        """Executes line 25 (True condition) and line 26 (raise ValueError)."""
        with pytest.raises(ValueError, match="coupon only for first order"):
            apply_coupon(300, "WELCOME", False)

    def test_apply_coupon_order_below_minimum(self):
        """Executes line 27 (True condition) and line 28 (return order_value)."""
        assert apply_coupon(150, "SAVE50", True) == 150

    def test_apply_coupon_valid_discount_applied(self):
        """Executes line 29 (return order_value - COUPONS[code])."""
        assert apply_coupon(300, "SAVE50", True) == 250


class TestEstimatedTimeCodeCoverage:
    """Tests designed to execute every line of estimated_time."""

    def test_estimated_time_peak_hour_and_busy(self):
        """
        Executes line 33 (base time calculation: 15 + 5*4 = 35),
        line 34-35 (peak hour: +10),
        line 36-37 (restaurant busy: +15),
        line 38-39 (peak hour during busy: +5),
        and line 40 (return minutes = 65).
        """
        assert estimated_time(5, is_peak_hour=True, restaurant_busy=True) == 65
