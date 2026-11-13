"""
Food Delivery Application Module (Hardened & Fuzz-Tested).

Course: Software Engineering Lab 7 - Fuzzing for Input Validation Bugs
Student: Rudra Dhadhal (PES1UG24CS146)
"""

import math
import re


def parse_order(items_csv):
    """
    Parse a comma-separated list of items and quantities (e.g. 'pizza:2,burger:1').
    Returns a dictionary mapping item names to integer quantities.
    Hardened against invalid types, empty strings, missing colons, invalid numbers,
    and malformed CSV inputs.
    """
    order = {}
    if not isinstance(items_csv, str):
        return order

    for item in items_csv.split(','):
        item = item.strip()
        if not item or ':' not in item:
            continue
        parts = item.split(':')
        if len(parts) != 2:
            continue
        name, qty_str = parts[0].strip(), parts[1].strip()
        if not name:
            continue
        try:
            qty = int(qty_str)
            if qty > 0:
                order[name] = order.get(name, 0) + qty
        except (ValueError, TypeError):
            continue

    return order


def delivery_eta(distance_km):
    """
    Calculate estimated delivery arrival time in minutes.
    Formula: 15 minutes base time + 4 minutes per km.
    Returns integer minutes.
    Hardened against None, non-numeric values, negative distances, NaN, infinity,
    and extreme values.
    """
    if distance_km is None:
        return 0

    try:
        dist = float(distance_km)
    except (ValueError, TypeError):
        return 0

    if math.isnan(dist) or math.isinf(dist) or dist < 0 or dist > 10000:
        return 0

    return int(15 + dist * 4)


def coupon_discount(code):
    """
    Extract discount amount from a promotional coupon code (e.g. 'SAVE50' -> 50).
    Returns integer discount amount.
    Hardened against None, non-strings, missing 'SAVE' prefix, non-digit values,
    and malformed codes.
    """
    if not isinstance(code, str):
        return 0

    code_clean = code.strip().upper()
    match = re.search(r'SAVE(\d+)', code_clean)
    if match:
        try:
            return int(match.group(1))
        except (ValueError, TypeError):
            return 0

    return 0


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter items as name:qty CSV (e.g. pizza:2,burger:1): ")
    result = parse_order(user_input)
    print("Order:", result)

    print("\n==== Running delivery_eta ====")
    user_input = input("Enter distance in km (e.g. 4.5): ")
    result = delivery_eta(user_input)
    print("ETA in Minutes:", result)

    print("\n==== Running coupon_discount ====")
    user_input = input("Enter a coupon code (e.g. SAVE50): ")
    result = coupon_discount(user_input)
    print("Discount:", result)


if __name__ == "__main__":
    main()
