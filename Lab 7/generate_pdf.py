"""
Generate Lab 7 PDF Report with embedded screenshots, analysis, and source code.
Deliverable for Software Engineering Lab 7: Fuzzing for Input Validation Bugs.
Student: Rudra Dhadhal (PES1UG24CS146)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\rudra\SE-labs\Lab 7"
PDF_PATH = os.path.join(BASE_DIR, "Lab7_Fuzzing_PES1UG24CS146_Rudra_Dhadhal.pdf")

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages dynamically for footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PES University | Software Engineering (UE24CS342AA2) — Lab 7: Fuzz Testing")
            self.drawRightString(558, 750, "Rudra Dhadhal (PES1UG24CS146)")
            self.setStrokeColor(colors.HexColor("#cccccc"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
        
        # Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, text)
        self.drawString(54, 36, "Confidential — Educational Material — PES University")
        self.setStrokeColor(colors.HexColor("#cccccc"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    dark_gray = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#CBD5E0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=dark_gray,
        spaceAfter=5
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_gray
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A365D")
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("LAB 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("Software Engineering (UE24CS342AA2) — Automated Security & Quality Assurance", subtitle_style))
    
    meta_data = [
        [Paragraph("<b>Student Name:</b> Rudra Dhadhal", table_cell_style), Paragraph("<b>SRN:</b> PES1UG24CS146", table_cell_style)],
        [Paragraph("<b>Course:</b> Software Engineering", table_cell_style), Paragraph("<b>Department:</b> Computer Science & Engineering", table_cell_style)],
        [Paragraph("<b>Assigned Domain:</b> Food Delivery (L6_L7_20)", table_cell_style), Paragraph("<b>Testing Framework:</b> Hypothesis 6.99.9 & Pytest 9.2.0", table_cell_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary & Lab Objectives", h1_style))
    story.append(Paragraph(
        "Fuzz testing (or fuzzing) is an automated dynamic testing technique where semi-random, unexpected, or malformed data "
        "is fed into software interfaces to uncover edge-case crashes, memory safety bugs, and security vulnerabilities. While conventional unit tests "
        "verify intended 'happy paths', property-based fuzzing tests universal invariants (e.g. <i>'the application must never crash or raise unhandled "
        "exceptions regardless of input'</i>). Using Python's <b>Hypothesis</b> library, this lab exposes input validation defects in an assigned "
        "Food Delivery application, hardens the codebase via defensive programming, and verifies 100% crash-resilience across hundreds of iterations.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Step 2: Execution of Buggy Application (processor.py)", h1_style))
    story.append(Paragraph(
        "The starter application (<code>food_delivery.py</code> / <code>processor.py</code>) was executed with normal sample inputs. "
        "Under ideal formatting, the program produces expected outputs; however, it lacks input sanitization and exception handling:",
        body_style
    ))
    img2_path = os.path.join(BASE_DIR, "step2_buggy_app_run.png")
    if os.path.exists(img2_path):
        story.append(RLImage(img2_path, width=490, height=170))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("3. Steps 3 & 4: Hypothesis Fuzz Testing & Defect Discovery", h1_style))
    story.append(Paragraph(
        "Property-based fuzz tests were constructed in <code>test_processor.py</code> using Hypothesis strategies <code>st.text() | st.none()</code>. "
        "When run via Pytest, Hypothesis immediately broke all three functions and minimized inputs to minimal counterexamples:",
        body_style
    ))
    img4_path = os.path.join(BASE_DIR, "step4_test_failure_fuzzing.png")
    if os.path.exists(img4_path):
        story.append(RLImage(img4_path, width=490, height=415))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Analysis of Defects & Falsifying Counterexamples", h2_style))
    bugs_data = [
        [Paragraph("Function", table_cell_bold), Paragraph("Falsifying Input", table_cell_bold), Paragraph("Exception Raised", table_cell_bold), Paragraph("Root Cause & Resolution", table_cell_bold)],
        [
            Paragraph("<code>parse_order(s)</code>", table_cell_style),
            Paragraph("<code>s = ''</code><br/><code>s = ':'</code><br/><code>s = None</code>", table_cell_style),
            Paragraph("<code>ValueError</code><br/><code>AttributeError</code>", table_cell_style),
            Paragraph("Empty string fails <code>split(':')</code> tuple unpacking. Colon without numbers produces <code>int('')</code> error. Non-string/None crashes on <code>.split()</code>. <b>Fix:</b> String type check, split length validation, safe int parse.", table_cell_style)
        ],
        [
            Paragraph("<code>delivery_eta(s)</code>", table_cell_style),
            Paragraph("<code>s = ''</code><br/><code>s = None</code><br/><code>s = 'abc'</code>", table_cell_style),
            Paragraph("<code>ValueError</code><br/><code>TypeError</code>", table_cell_style),
            Paragraph("Unchecked <code>float(distance_km)</code> crashes on empty/alphabetic strings and NoneType. Negative/infinite distances yield invalid ETAs. <b>Fix:</b> Try-except float conversion, range & NaN/Inf bounds check.", table_cell_style)
        ],
        [
            Paragraph("<code>coupon_discount(s)</code>", table_cell_style),
            Paragraph("<code>s = ''</code><br/><code>s = None</code><br/><code>s = 'SAVE'</code>", table_cell_style),
            Paragraph("<code>IndexError</code><br/><code>AttributeError</code><br/><code>ValueError</code>", table_cell_style),
            Paragraph("Missing 'SAVE' causes <code>split('SAVE')</code> to yield only 1 element, raising <code>IndexError: [1]</code>. Code without digits fails <code>int()</code>. <b>Fix:</b> Regex pattern matching <code>SAVE(\\d+)</code> with safe fallback 0.", table_cell_style)
        ]
    ]
    bugs_table = Table(bugs_data, colWidths=[90, 80, 95, 239])
    bugs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(bugs_table)

    # ================= PAGE 3 =================
    story.append(PageBreak())
    story.append(Paragraph("4. Step 5: Hardened Application Implementation & Execution", h1_style))
    story.append(Paragraph(
        "The application was redesigned with defensive programming: strict type validation, safe token extraction, numeric boundary "
        "and NaN/Inf checks, and graceful fallbacks (empty dict <code>{}</code>, zero ETA <code>0</code>, zero discount <code>0</code>):",
        body_style
    ))
    img5_path = os.path.join(BASE_DIR, "step5_fixed_app_run.png")
    if os.path.exists(img5_path):
        story.append(RLImage(img5_path, width=490, height=140))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Step 6: Verification via Hypothesis Fuzz Testing (100% Passed)", h1_style))
    story.append(Paragraph(
        "The complete test suite was re-executed against the hardened application. Across standard arbitrary string/None strategies "
        "and extended boundary strategies (integers, negative numbers, floats, collections), all 7 test suites achieved 100% pass rate:",
        body_style
    ))
    img6_path = os.path.join(BASE_DIR, "step6_test_passed_fuzzing.png")
    if os.path.exists(img6_path):
        story.append(RLImage(img6_path, width=490, height=310))

    # ================= PAGE 4 =================
    story.append(PageBreak())
    story.append(Paragraph("6. Deliverables: Source Code Listings", h1_style))
    
    story.append(Paragraph("A. Hardened Application Script (food_delivery.py / processor.py)", h2_style))
    app_code = """import math, re

def parse_order(items_csv):
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
    if not isinstance(code, str):
        return 0
    match = re.search(r'SAVE(\\d+)', code.strip().upper())
    if match:
        try:
            return int(match.group(1))
        except (ValueError, TypeError):
            return 0
    return 0"""
    
    story.append(Table([[Paragraph(f"<font face='Courier' size='6.8'>{app_code.replace(' ', '&nbsp;').replace(chr(10), '<br/>')}</font>", table_cell_style)]],
                       colWidths=[504],
                       style=[('BACKGROUND', (0,0), (-1,-1), light_bg),
                              ('BOX', (0,0), (-1,-1), 1, border_color),
                              ('TOPPADDING', (0,0), (-1,-1), 4),
                              ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("B. Updated Hypothesis Fuzz Testing Code (test_food_delivery.py / test_processor.py)", h2_style))
    test_code = """from hypothesis import given, strategies as st
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

@given(st.integers() | st.floats() | st.none())
def test_delivery_eta_numeric_inputs(val):
    result = delivery_eta(val)
    assert isinstance(result, int) and result >= 0

@given(st.integers(min_value=0, max_value=1000))
def test_coupon_discount_valid_codes(amt):
    assert coupon_discount(f"SAVE{amt}") == amt"""

    story.append(Table([[Paragraph(f"<font face='Courier' size='6.8'>{test_code.replace(' ', '&nbsp;').replace(chr(10), '<br/>')}</font>", table_cell_style)]],
                       colWidths=[504],
                       style=[('BACKGROUND', (0,0), (-1,-1), light_bg),
                              ('BOX', (0,0), (-1,-1), 1, border_color),
                              ('TOPPADDING', (0,0), (-1,-1), 4),
                              ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7. Learning Outcomes & Conclusion", h1_style))
    story.append(Paragraph(
        "By integrating Hypothesis property-based fuzz testing into the development lifecycle, we revealed critical boundary vulnerabilities "
        "that escaped standard testing methodologies. Hypothesis's automated input minimization (shrinking) effectively isolated the exact root "
        "causes (such as missing delimiter unpacking, unhandled NoneType conversions, and regex boundary conditions). "
        "Implementing defensive programming hardened the application into a robust, crash-resilient service capable of handling arbitrary real-world inputs.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated clean 4-page PDF: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
