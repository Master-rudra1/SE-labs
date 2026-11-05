"""
Branch Coverage Test Suite for Food Delivery Application
Author: Rudra Dhadhal (SRN: PES1UG24CS146)
Lab 6: Code and Branch Coverage Analysis

Objective:
This test suite is designed to achieve 100% Branch Coverage on `food_delivery.py`
(exceeding the >= 90% threshold required by the rubric).
Every control structure (`if`, `elif`, `else`), boolean operator (`or`, `and`, `not`),
and edge boundary condition evaluates to both True and False outcomes with 0 missing branches.
"""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


class TestDeliveryChargeBranchCoverage:
    """Comprehensive branch and boundary condition tests for delivery_charge."""

    def test_distance_boundary_zero(self):
        """Branch: distance_km <= 0 (boundary at exactly 0)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(0, 300, False)

    def test_distance_negative(self):
        """Branch: distance_km <= 0 (strictly negative)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(-5, 300, False)

    def test_distance_above_maximum_boundary(self):
        """Branch: distance_km > 15 (boundary above 15, e.g., 15.1 and 16)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(16, 300, False)

    def test_distance_maximum_valid_boundary(self):
        """Branch: distance_km == 15 (upper valid boundary, evaluates condition False)."""
        assert delivery_charge(15, 300, False) == 60

    def test_distance_minimum_valid_boundary(self):
        """Branch: distance_km == 0.1 (lower valid boundary, evaluates condition False)."""
        assert delivery_charge(0.1, 300, False) == 20

    def test_order_value_exactly_500_no_rain(self):
        """Branch: order_value >= 500 (boundary True), is_raining = False."""
        assert delivery_charge(5, 500, is_raining=False) == 0

    def test_order_value_above_500_with_rain(self):
        """Branch: order_value >= 500 (True), is_raining = True (+30 surcharge)."""
        assert delivery_charge(5, 750, is_raining=True) == 30

    def test_order_value_below_500_falls_through(self):
        """Branch: order_value >= 500 (boundary False, 499) -> falls to distance tiers."""
        assert delivery_charge(2, 499, is_raining=False) == 20

    def test_tier_short_distance_boundary_3_no_rain(self):
        """Branch: distance_km <= 3 (boundary True at 3), is_raining = False."""
        assert delivery_charge(3, 200, is_raining=False) == 20

    def test_tier_short_distance_with_rain(self):
        """Branch: distance_km <= 3 (True at 1), is_raining = True (+30)."""
        assert delivery_charge(1, 200, is_raining=True) == 50

    def test_tier_medium_distance_boundary_8_no_rain(self):
        """Branch: distance_km <= 8 (boundary True at 8), is_raining = False."""
        assert delivery_charge(8, 200, is_raining=False) == 40

    def test_tier_medium_distance_with_rain(self):
        """Branch: distance_km <= 8 (True at 5), is_raining = True (+30)."""
        assert delivery_charge(5, 200, is_raining=True) == 70

    def test_tier_long_distance_else_branch_no_rain(self):
        """Branch: distance_km > 8 (else branch True at 12), is_raining = False."""
        assert delivery_charge(12, 200, is_raining=False) == 60

    def test_tier_long_distance_else_branch_with_rain(self):
        """Branch: distance_km > 8 (else branch True at 15), is_raining = True (+30)."""
        assert delivery_charge(15, 200, is_raining=True) == 90


class TestApplyCouponBranchCoverage:
    """Comprehensive branch and compound condition tests for apply_coupon."""

    def test_coupon_none_first_order(self):
        """Branch: code is None (True, is_first_order=True)."""
        assert apply_coupon(350, None, is_first_order=True) == 350

    def test_coupon_none_returning_order(self):
        """Branch: code is None (True, is_first_order=False)."""
        assert apply_coupon(350, None, is_first_order=False) == 350

    def test_coupon_not_in_coupons(self):
        """Branch: code not in COUPONS (True) -> raises ValueError."""
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(350, "FLAT50", is_first_order=True)

    def test_coupon_welcome_returning_customer_rejected(self):
        """
        Compound Branch: code == 'WELCOME' (True) and not is_first_order (True)
        -> raises ValueError.
        """
        with pytest.raises(ValueError, match="coupon only for first order"):
            apply_coupon(350, "WELCOME", is_first_order=False)

    def test_coupon_welcome_first_order_below_200(self):
        """
        Compound Branch: code == 'WELCOME' (True) and not is_first_order (False)
        order_value < 200 (True at 150) -> returns undiscounted value.
        """
        assert apply_coupon(150, "WELCOME", is_first_order=True) == 150

    def test_coupon_welcome_first_order_at_boundary_200(self):
        """
        Branch: order_value < 200 (False at boundary 200) -> applies 100 off.
        """
        assert apply_coupon(200, "WELCOME", is_first_order=True) == 100

    def test_coupon_welcome_first_order_above_200(self):
        """Branch: WELCOME applied to eligible first order (> 200)."""
        assert apply_coupon(400, "WELCOME", is_first_order=True) == 300

    def test_coupon_save50_returning_customer_below_200(self):
        """
        Compound Branch: code != 'WELCOME' (SAVE50), not is_first_order (True)
        order_value < 200 (True at 199) -> returns undiscounted value.
        """
        assert apply_coupon(199, "SAVE50", is_first_order=False) == 199

    def test_coupon_save50_returning_customer_eligible(self):
        """
        Compound Branch: SAVE50 with is_first_order=False (order_value >= 200)
        -> applies 50 discount.
        """
        assert apply_coupon(250, "SAVE50", is_first_order=False) == 200

    def test_coupon_save50_first_order_eligible(self):
        """
        Compound Branch: SAVE50 with is_first_order=True (order_value >= 200)
        -> applies 50 discount.
        """
        assert apply_coupon(250, "SAVE50", is_first_order=True) == 200


class TestEstimatedTimeBranchCoverage:
    """Comprehensive branch tests covering all decision permutations in estimated_time."""

    def test_offpeak_not_busy(self):
        """
        Branch: is_peak_hour = False, restaurant_busy = False
        minutes = 15 + (3 * 4) = 27.
        """
        assert estimated_time(3, is_peak_hour=False, restaurant_busy=False) == 27

    def test_peak_hour_not_busy(self):
        """
        Branch: is_peak_hour = True (+10), restaurant_busy = False
        minutes = 15 + (3 * 4) + 10 = 37.
        """
        assert estimated_time(3, is_peak_hour=True, restaurant_busy=False) == 37

    def test_offpeak_restaurant_busy(self):
        """
        Branch: is_peak_hour = False (+0), restaurant_busy = True (+15)
        Nested Branch: is_peak_hour = False (+0)
        minutes = 15 + (3 * 4) + 15 = 42.
        """
        assert estimated_time(3, is_peak_hour=False, restaurant_busy=True) == 42

    def test_peak_hour_restaurant_busy(self):
        """
        Branch: is_peak_hour = True (+10), restaurant_busy = True (+15)
        Nested Branch: is_peak_hour = True (+5 extra)
        minutes = 15 + (3 * 4) + 10 + 15 + 5 = 57.
        """
        assert estimated_time(3, is_peak_hour=True, restaurant_busy=True) == 57
