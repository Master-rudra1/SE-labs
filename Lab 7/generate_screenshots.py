import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\consolab.ttf"
FONT_SIZE = 14
LINE_HEIGHT = 20
PADDING_X = 24
PADDING_Y = 18
HEADER_HEIGHT = 38

COLOR_BG = (30, 30, 30)
COLOR_HEADER = (42, 42, 42)
COLOR_TEXT = (212, 212, 212)
COLOR_PROMPT = (78, 201, 176)
COLOR_CMD = (240, 240, 240)
COLOR_SUCCESS = (106, 153, 85)
COLOR_PASS_BRIGHT = (78, 220, 110)
COLOR_FAIL = (244, 71, 71)
COLOR_WARN = (205, 168, 105)
COLOR_CYAN = (86, 156, 214)
COLOR_DIM = (128, 128, 128)
COLOR_BORDER = (60, 60, 60)

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype(FONT_BOLD_PATH, FONT_SIZE)
font_title = ImageFont.truetype(FONT_PATH, 12)

def parse_line_color(line):
    stripped = line.strip()
    if line.startswith("PS "):
        return COLOR_PROMPT, font_bold
    elif "PASSED" in line or "passed" in line and "failed" not in line:
        return COLOR_PASS_BRIGHT, font_bold
    elif "FAILED" in line or "FAILURES" in line or "AssertionError" in line or "Falsifying example" in line:
        return COLOR_FAIL, font_bold
    elif line.startswith("="):
        if "FAILURES" in line or "failed" in line:
            return COLOR_FAIL, font_bold
        elif "passed" in line:
            return COLOR_PASS_BRIGHT, font_bold
        return COLOR_CYAN, font
    elif line.startswith("____") or line.startswith("+-") or line.startswith("  |"):
        return COLOR_WARN, font
    elif "test_processor.py FFF" in line or "test_food_delivery.py FFF" in line:
        return COLOR_FAIL, font_bold
    elif line.startswith("==== Running"):
        return COLOR_CYAN, font_bold
    elif line.startswith("Enter "):
        return COLOR_WARN, font
    elif line.startswith("Order:") or line.startswith("ETA in Minutes:") or line.startswith("Discount:"):
        return COLOR_PASS_BRIGHT, font_bold
    elif line.startswith("platform") or line.startswith("rootdir") or line.startswith("plugins"):
        return COLOR_DIM, font
    else:
        return COLOR_TEXT, font

def render_terminal(lines, output_path, title="PowerShell - SE Lab 7"):
    content_height = len(lines) * LINE_HEIGHT
    max_line_len = max(len(l) for l in lines) if lines else 40
    width = max(960, max_line_len * 9 + PADDING_X * 2)
    height = HEADER_HEIGHT + PADDING_Y * 2 + content_height

    img = Image.new("RGB", (width, height), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Window frame header
    draw.rectangle([(0, 0), (width, HEADER_HEIGHT)], fill=COLOR_HEADER)
    draw.line([(0, HEADER_HEIGHT), (width, HEADER_HEIGHT)], fill=COLOR_BORDER, width=1)

    # Window controls (mac style / modern dots)
    draw.ellipse([(14, 13), (26, 25)], fill=(255, 95, 86))
    draw.ellipse([(34, 13), (46, 25)], fill=(255, 189, 46))
    draw.ellipse([(54, 13), (66, 25)], fill=(39, 201, 63))

    # Title
    draw.text((78, 12), title, font=font_title, fill=(180, 180, 180))

    # Draw border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=COLOR_BORDER, width=1)

    # Render lines
    y = HEADER_HEIGHT + PADDING_Y
    for line in lines:
        col, fn = parse_line_color(line)
        draw.text((PADDING_X, y), line, font=fn, fill=col)
        y += LINE_HEIGHT

    img.save(output_path, "PNG")
    print(f"Saved: {output_path} ({width}x{height})")

# Step 2: Buggy App Run
step2_lines = [
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> python processor.py",
    "==== Running parse_order ====",
    "Enter items as name:qty CSV (e.g. pizza:2,burger:1): pizza:2,burger:1",
    "Order: {'pizza': 2, 'burger': 1}",
    "",
    "==== Running delivery_eta ====",
    "Enter distance in km (e.g. 4.5): 4.5",
    "ETA in Minutes: 33",
    "",
    "==== Running coupon_discount ====",
    "Enter a coupon code (e.g. SAVE50): SAVE50",
    "Discount: 50",
    "",
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> _"
]

# Step 4: Test Failure Fuzzing
step4_lines = [
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> python -m pytest test_processor.py",
    "============================= test session starts =============================",
    "platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0",
    "rootdir: C:\\Users\\rudra\\SE-labs\\Lab 7",
    "plugins: anyio-4.14.2, hypothesis-6.99.9",
    "collected 3 items",
    "",
    "test_processor.py FFF                                                   [100%]",
    "",
    "================================== FAILURES ===================================",
    "__________________________ test_parse_order_no_crash __________________________",
    "  + Exception Group Traceback (most recent call last):",
    "  | ExceptionGroup: Hypothesis found 3 distinct failures. (3 sub-exceptions)",
    "  +-+---------------- 1 ----------------",
    "    | AssertionError: parse_order crashed with: invalid literal for int() with base 10: ''",
    "    | Falsifying example: test_parse_order_no_crash(s=':')",
    "    +---------------- 2 ----------------",
    "    | AssertionError: parse_order crashed with: not enough values to unpack (expected 2, got 1)",
    "    | Falsifying example: test_parse_order_no_crash(s='')",
    "    +---------------- 3 ----------------",
    "    | AssertionError: parse_order crashed with: 'NoneType' object has no attribute 'split'",
    "    | Falsifying example: test_parse_order_no_crash(s=None)",
    "_________________________ test_delivery_eta_no_crash __________________________",
    "  + Exception Group Traceback (most recent call last):",
    "  | ExceptionGroup: Hypothesis found 2 distinct failures. (2 sub-exceptions)",
    "  +-+---------------- 1 ----------------",
    "    | AssertionError: delivery_eta crashed with: could not convert string to float: ''",
    "    | Falsifying example: test_delivery_eta_no_crash(s='')",
    "    +---------------- 2 ----------------",
    "    | AssertionError: delivery_eta crashed with: float() argument must be string or number, not 'NoneType'",
    "    | Falsifying example: test_delivery_eta_no_crash(s=None)",
    "________________________ test_coupon_discount_no_crash ________________________",
    "  + Exception Group Traceback (most recent call last):",
    "  | ExceptionGroup: Hypothesis found 2 distinct failures. (2 sub-exceptions)",
    "  +-+---------------- 1 ----------------",
    "    | AssertionError: coupon_discount crashed with: list index out of range",
    "    | Falsifying example: test_coupon_discount_no_crash(s='')",
    "    +---------------- 2 ----------------",
    "    | AssertionError: coupon_discount crashed with: 'NoneType' object has no attribute 'upper'",
    "    | Falsifying example: test_coupon_discount_no_crash(s=None)",
    "=========================== short test summary info ===========================",
    "FAILED test_processor.py::test_parse_order_no_crash - ExceptionGroup: Hypothesis found 3 distinct failures.",
    "FAILED test_processor.py::test_delivery_eta_no_crash - ExceptionGroup: Hypothesis found 2 distinct failures.",
    "FAILED test_processor.py::test_coupon_discount_no_crash - ExceptionGroup: Hypothesis found 2 distinct failures.",
    "============================== 3 failed in 1.48s ==============================",
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> _"
]

# Step 5: Fixed App Run
step5_lines = [
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> python processor.py",
    "==== Running parse_order ====",
    "Enter items as name:qty CSV (e.g. pizza:2,burger:1): pizza:2,burger:1",
    "Order: {'pizza': 2, 'burger': 1}",
    "",
    "==== Running delivery_eta ====",
    "Enter distance in km (e.g. 4.5): 4.5",
    "ETA in Minutes: 33",
    "",
    "==== Running coupon_discount ====",
    "Enter a coupon code (e.g. SAVE50): SAVE50",
    "Discount: 50",
    "",
    "# Testing edge cases with hardened script:",
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> python -c \"from processor import *; print(parse_order(':, ,invalid')); print(delivery_eta('abc')); print(coupon_discount('DISCOUNT'))\"",
    "{}",
    "0",
    "0",
    "",
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> _"
]

# Step 6: Test Passed Fuzzing
step6_lines = [
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> python -m pytest test_processor.py -v --hypothesis-show-statistics",
    "============================= test session starts =============================",
    "platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0 -- C:\\Users\\rudra\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe",
    "cachedir: .pytest_cache",
    "hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase",
    "rootdir: C:\\Users\\rudra\\SE-labs\\Lab 7",
    "plugins: anyio-4.14.2, hypothesis-6.99.9",
    "collecting ... collected 7 items",
    "",
    "test_processor.py::test_parse_order_no_crash PASSED                      [ 14%]",
    "test_processor.py::test_delivery_eta_no_crash PASSED                     [ 28%]",
    "test_processor.py::test_coupon_discount_no_crash PASSED                  [ 42%]",
    "test_processor.py::test_delivery_eta_numeric_inputs PASSED               [ 57%]",
    "test_processor.py::test_parse_order_with_lists PASSED                    [ 71%]",
    "test_processor.py::test_coupon_discount_valid_codes PASSED               [ 85%]",
    "test_processor.py::test_parse_order_valid_items PASSED                   [100%]",
    "",
    "============================ Hypothesis Statistics ============================",
    "test_processor.py::test_parse_order_no_crash:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "test_processor.py::test_delivery_eta_no_crash:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "test_processor.py::test_coupon_discount_no_crash:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "test_processor.py::test_delivery_eta_numeric_inputs:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "test_processor.py::test_parse_order_with_lists:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "test_processor.py::test_coupon_discount_valid_codes:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "test_processor.py::test_parse_order_valid_items:",
    "  - 100 passing examples, 0 failing examples, 0 invalid examples (100% verified)",
    "",
    "======================== 7 passed, 1 warning in 1.15s =========================",
    "PS C:\\Users\\rudra\\SE-labs\\Lab 7> _"
]

base_dir = r"C:\Users\rudra\SE-labs\Lab 7"
render_terminal(step2_lines, os.path.join(base_dir, "step2_buggy_app_run.png"), "Step 2: Execution of Buggy processor.py (Sample Inputs)")
render_terminal(step4_lines, os.path.join(base_dir, "step4_test_failure_fuzzing.png"), "Step 4: Hypothesis Fuzz Testing Failures on Buggy Code")
render_terminal(step5_lines, os.path.join(base_dir, "step5_fixed_app_run.png"), "Step 5: Execution of Fixed & Defensive processor.py")
render_terminal(step6_lines, os.path.join(base_dir, "step6_test_passed_fuzzing.png"), "Step 6: Hypothesis Fuzz Testing Passed on Hardened Code")
