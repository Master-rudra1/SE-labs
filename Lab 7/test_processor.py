"""
Test Processor alias / wrapper conforming to generic lab handout naming convention.
Imports and runs all tests from test_food_delivery.py.
"""

from test_food_delivery import (
    test_parse_order_no_crash,
    test_delivery_eta_no_crash,
    test_coupon_discount_no_crash,
    test_delivery_eta_numeric_inputs,
    test_parse_order_with_lists,
    test_coupon_discount_valid_codes,
    test_parse_order_valid_items,
)
