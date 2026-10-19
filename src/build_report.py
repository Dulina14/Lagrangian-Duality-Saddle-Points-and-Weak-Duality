from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from pypdf import PdfReader, PdfWriter
import io
import os
import matplotlib

# Paths relative to the repository root
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FIG = os.path.join(ROOT, "figures")
SRC_PDF = os.path.join(ROOT, "source", "answers_handwritten.pdf")
OUT_PDF = os.path.join(ROOT, "report", "220511N_EN3330_A03.pdf")
REPO_URL = "https://github.com/Dulina14/Lagrangian-Duality-Saddle-Points-and-Weak-Duality"

# DejaVu fonts ship with matplotlib, so this works on Windows, macOS and Linux
D = os.path.join(matplotlib.get_data_path(), "fonts", "ttf") + os.sep
pdfmetrics.registerFont(TTFont("Serif", D + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", D + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-I", D + "DejaVuSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BI", D + "DejaVuSerif-BoldItalic.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")

W, H = 612, 866.0571
body = ParagraphStyle("b", fontName="Serif", fontSize=10.5, leading=15, alignment=TA_JUSTIFY)
cap = ParagraphStyle("c", fontName="Serif", fontSize=9.5, leading=13, alignment=TA_JUSTIFY)
head = ParagraphStyle("h", fontName="Serif-B", fontSize=11.5, leading=16)


def new_canvas():
    buf = io.BytesIO()
    return buf, canvas.Canvas(buf, pagesize=(W, H))


def done(buf, c):
    c.showPage(); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]


def draw_par(c, text, style, x, y_top, width):
    p = Paragraph(text, style)
    _, h = p.wrap(width, H)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def figure_page(title, figs):
    """figs: list of (png, caption, width)"""
    buf, c = new_canvas()
    margin = 60
    y = H - 55
    y = draw_par(c, title, head, margin, y, W - 2 * margin) - 14
    for png, caption, w in figs:
        img = ImageReader(os.path.join(FIG, png))
        iw, ih = img.getSize()
        h = w * ih / iw
        x = (W - w) / 2
        c.drawImage(img, x, y - h, w, h)
        y -= h + 6
        y = draw_par(c, caption, cap, margin + 10, y, W - 2 * margin - 20) - 22
    return done(buf, c)


def cover_page():
    buf, c = new_canvas()
    cx = W / 2
    def centre(txt, y, font="Serif", size=12):
        c.setFont(font, size); c.drawCentredString(cx, y, txt)
    centre("University of Moratuwa", H - 120, "Serif-B", 17)
    centre("Department of Electronic and Telecommunication Engineering", H - 145, "Serif", 12)
    c.setStrokeColor(colors.HexColor("#444444")); c.setLineWidth(0.8)
    c.line(90, H - 170, W - 90, H - 170)
    centre("EN3330 – Introduction to Engineering Optimization", H - 250, "Serif-B", 15)
    centre("Assignment 03", H - 290, "Serif-B", 22)
    centre("Lagrangian Duality, Saddle Points and Weak Duality", H - 320, "Serif-I", 13)
    c.line(90, H - 360, W - 90, H - 360)

    rows = [["Name", "Ranaweera R.P.D.D.H."],
            ["Index No.", "220511N"],
            ["Module", "EN3330 – Introduction to Engineering Optimization"],
            ["Lecturer", "M. T. U. Sampath K. Perera"],
            ["Date of Submission", "19 October 2026"]]
    t = Table(rows, colWidths=[130, 290], rowHeights=26)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Serif-B"),
        ("FONTNAME", (1, 0), (1, -1), "Serif"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#bbbbbb")),
    ]))
    tw, th = t.wrap(0, 0)
    t.drawOn(c, (W - tw) / 2, H - 420 - th)

    # Source code link (clickable)
    y = H - 420 - th - 60
    centre("Source code, figures and report:", y, "Serif-B", 11)
    c.setFillColor(colors.HexColor("#1a4fa0"))
    c.setFont("Serif", 10)
    c.drawCentredString(cx, y - 18, REPO_URL)
    lw = pdfmetrics.stringWidth(REPO_URL, "Serif", 10)
    c.setStrokeColor(colors.HexColor("#1a4fa0")); c.setLineWidth(0.5)
    c.line(cx - lw / 2, y - 20, cx + lw / 2, y - 20)
    c.linkURL(REPO_URL, (cx - lw / 2, y - 22, cx + lw / 2, y - 8), relative=0)
    c.setFillColor(colors.black)
    return done(buf, c)


def q3b_overlay():
    """Typed Q3(b) answer, placed in the blank area under the handwritten '(b)' on page 10."""
    buf, c = new_canvas()
    x, wdt = 62, W - 62 - 50
    y = H - 222
    paras = [
        "For a fixed <i>x</i>, the Lagrangian <i>L</i>(<i>μ</i>, <i>x</i>) = <i>x</i><super>2</super> + <i>μ</i>(1 − <i>x</i>) "
        "is a straight line in <i>μ</i>, with intercept <i>x</i><super>2</super> and slope (1 − <i>x</i>):",
    ]
    for p in paras:
        y = draw_par(c, p, body, x, y, wdt) - 8

    rows = [["x", "L(μ, x)", "Intercept", "Slope"],
            ["0", "μ", "0", "+1 (rising)"],
            ["1", "1", "1", "0 (flat)"],
            ["2", "4 − μ", "4", "−1 (falling)"]]
    t = Table(rows, colWidths=[50, 90, 80, 110], rowHeights=19)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Serif-B"), ("FONTNAME", (0, 1), (-1, -1), "Serif"),
        ("FONTSIZE", (0, 0), (-1, -1), 10), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black)]))
    tw, th = t.wrap(0, 0)
    t.drawOn(c, x + (wdt - tw) / 2, y - th)
    y -= th + 12

    more = [
        "The lines for <i>x</i> = 0 and <i>x</i> = 1 cross at <i>μ</i> = 1, and the lines for <i>x</i> = 1 and "
        "<i>x</i> = 2 cross at <i>μ</i> = 3. Taking the lowest line at each <i>μ</i> gives the lower envelope "
        "(thick black line in Figure 5):",
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>E</i>(<i>μ</i>) = <i>μ</i> for 0 ≤ <i>μ</i> ≤ 1, &nbsp; <i>E</i>(<i>μ</i>) = 1 for "
        "1 ≤ <i>μ</i> ≤ 3, &nbsp; <i>E</i>(<i>μ</i>) = 4 − <i>μ</i> for <i>μ</i> ≥ 3.",
        "<b>Concave or convex?</b> The envelope rises, stays flat and then falls, giving a “tent” (hill) shape, "
        "so it is <b>concave</b>. It lies on or above the true dual function <i>d</i>(<i>μ</i>) = <i>μ</i> − "
        "<i>μ</i><super>2</super>/4 (red dashed curve), because it uses only three values of <i>x</i> instead of "
        "minimising over all <i>x</i>. Each line touches <i>d</i>(<i>μ</i>) at one point, <i>μ</i> = 2<i>x</i> "
        "(at <i>μ</i> = 0, 2 and 4), so adding more values of <i>x</i> would make the envelope approach "
        "<i>d</i>(<i>μ</i>).",
        "<b>Why <i>d</i>(<i>μ</i>) is concave for any <i>f</i>:</b> for each fixed <i>x</i>, <i>f</i>(<i>x</i>) and "
        "<i>h</i>(<i>x</i>) are just numbers, so <i>L</i>(<i>μ</i>, <i>x</i>) = <i>f</i>(<i>x</i>) + "
        "<i>μ</i><i>h</i>(<i>x</i>) is always a straight line in <i>μ</i>, however complicated or non-convex "
        "<i>f</i> is. Since <i>d</i>(<i>μ</i>) is the pointwise minimum (lower envelope) of these lines, and the "
        "minimum of any set of straight lines can only bend downwards, <i>d</i>(<i>μ</i>) is always concave.",
        "<b>Interpretation:</b> because <i>d</i>(<i>μ</i>) is concave, any maximum found is the global maximum, "
        "so the dual problem is always a well-behaved problem, and by part (a) its value always gives a valid "
        "lower bound on <i>p</i>*.",
    ]
    for p in more:
        y = draw_par(c, p, body, x, y, wdt) - 9
    print("Q3b overlay bottom y =", round(y, 1))
    return done(buf, c)


src = PdfReader(SRC_PDF)
P = src.pages
out = PdfWriter()

f1 = figure_page("Figures for Question 1(a) and 1(b)", [
    ("Q1a_lagrangian_vs_x.png",
     "<b>Figure 1:</b> <i>L</i>(<i>μ</i>, <i>x</i>) = <i>x</i><super>2</super> + <i>μ</i>(1 − <i>x</i>) against <i>x</i> "
     "for <i>μ</i> = 0, 1, 2, 3. The dots mark the minimiser <i>x</i>(<i>μ</i>) = <i>μ</i>/2 of each curve, which "
     "moves right as <i>μ</i> increases and reaches the constraint boundary <i>x</i> = 1 at <i>μ</i> = 2. "
     "The shaded region (<i>x</i> &lt; 1) is infeasible.", 450),
    ("Q1b_dual_function.png",
     "<b>Figure 2:</b> Dual function <i>d</i>(<i>μ</i>) = <i>μ</i> − <i>μ</i><super>2</super>/4. It is concave, with "
     "its maximum at <i>μ</i>* = 2, where <i>d</i>* = 1 equals the primal optimum <i>p</i>* = 1 (dashed line), "
     "showing zero duality gap.", 450)])
f3 = figure_page("Figure for Question 1(c)", [
    ("Q1c_primal_function.png",
     "<b>Figure 3:</b> <i>L</i>(<i>μ</i>, <i>x</i>) against <i>x</i> for increasing <i>μ</i> = 0, 2, 5, 20, 100. "
     "For infeasible <i>x</i> &lt; 1 (shaded) the curves grow without limit as <i>μ</i> increases, so "
     "<i>g</i>(<i>x</i>) = +∞. For feasible <i>x</i> ≥ 1 the highest curve is the <i>μ</i> = 0 curve, so "
     "<i>g</i>(<i>x</i>) = <i>x</i><super>2</super> (thick black line). The minimum of <i>g</i> is 1 at "
     "<i>x</i>* = 1, the same as problem (1).", 480)])
f4 = figure_page("Figure for Question 2(a)(iv)", [
    ("Q2a_saddle_point.png",
     "<b>Figure 4:</b> Saddle point check. Left: <i>L</i>(<i>μ</i>, <i>x</i>*) = 1 for every <i>μ</i> (flat line), so "
     "no <i>μ</i> rises above <i>L</i>(<i>μ</i>*, <i>x</i>*) (left inequality). Right: <i>L</i>(<i>μ</i>*, <i>x</i>) = "
     "(<i>x</i> − 1)<super>2</super> + 1 has its lowest value at <i>x</i> = 1, so no <i>x</i> goes below it "
     "(right inequality). The red dots mark the common value <i>L</i>(<i>μ</i>*, <i>x</i>*) = 1.", 500)])
f5 = figure_page("Figure for Question 3(b)", [
    ("Q3b_lower_envelope.png",
     "<b>Figure 5:</b> <i>L</i>(<i>μ</i>, <i>x</i>) as a function of <i>μ</i> for <i>x</i> = 0, 1, 2 (straight lines). "
     "The thick black line is their lower envelope, which is concave (tent-shaped) and lies on or above the true "
     "dual function <i>d</i>(<i>μ</i>) = <i>μ</i> − <i>μ</i><super>2</super>/4 (red dashed curve).", 480)])

page10 = P[9]
page10.merge_page(q3b_overlay())

order = [cover_page(), P[0], P[1], P[2], f1, P[3], f3, P[4], f4,
         P[5], P[6], P[7], P[8], page10, f5, P[10]]
for pg in order:
    out.add_page(pg)
out.add_metadata({"/Title": "EN3330 Assignment 03", "/Author": "Ranaweera R.P.D.D.H. (220511N)"})
os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
with open(OUT_PDF, "wb") as fh:
    out.write(fh)
print("pages:", len(order))
