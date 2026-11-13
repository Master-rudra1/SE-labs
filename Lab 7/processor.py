"""
Processor alias / wrapper conforming to generic lab handout naming convention.
Delegates to food_delivery.py.
"""

from food_delivery import (
    parse_order,
    delivery_eta,
    coupon_discount,
    main,
)

if __name__ == "__main__":
    main()
