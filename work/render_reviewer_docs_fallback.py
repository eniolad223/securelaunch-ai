"""Render reviewer DOCX content to PDF for visual QA when LibreOffice is unavailable."""
from pathlib import Path

from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxParagraph
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs" / "reviewer_documents"
OUT = ROOT / "work" / "docx_pdfs"
OUT.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#24213D")
MUTED = colors.HexColor("#645D70")
PURPLE = colors.HexColor("#7152D6")
NAVY = colors.HexColor("#32304A")
LAVENDER = colors.HexColor("#EEE8FF")
PALE = colors.HexColor("#F7F5FB")
LINE = colors.HexColor("#D9D5E2")


def page_frame(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(0.72 * inch, 0.62 * inch, 7.78 * inch, 0.62 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.72 * inch, 0.40 * inch, "SecureLaunch AI | Eniola Durojaiye")
    canvas.drawRightString(7.78 * inch, 0.40 * inch, f"Page {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
TITLE = ParagraphStyle("TitleX", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=INK, spaceAfter=7)
SUBTITLE = ParagraphStyle("SubtitleX", parent=styles["Normal"], fontName="Helvetica", fontSize=11.5, leading=16, textColor=MUTED, spaceAfter=13)
H1 = ParagraphStyle("H1X", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=INK, spaceBefore=10, spaceAfter=5, keepWithNext=True)
BODY = ParagraphStyle("BodyX", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.2, textColor=INK, spaceAfter=4.5)
CALLOUT = ParagraphStyle("CalloutX", parent=BODY, backColor=LAVENDER, borderColor=colors.HexColor("#CFC1EA"), borderWidth=0.6, borderPadding=9, leftIndent=0, rightIndent=0, spaceBefore=3, spaceAfter=10)
CODE = ParagraphStyle("CodeX", parent=BODY, fontName="Courier", fontSize=8.3, leading=11.5, backColor=PALE, borderPadding=5, leftIndent=7, rightIndent=7, spaceAfter=1)
CELL = ParagraphStyle("CellX", parent=BODY, fontSize=8.0, leading=10.4, spaceAfter=0)
CELL_HEAD = ParagraphStyle("CellHeadX", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)


def safe(text):
    return escape(text).replace("\n", "<br/>")


def is_code(text):
    starts = ("preflight =", "if preflight", "return preflight", "trace_steps =", "raw_response =", "maskable =", "if finding.", "for finding", "replacement =", "protected =")
    return text.startswith(starts)


def render_table(table):
    rows = []
    for r_i, row in enumerate(table.rows):
        style = CELL_HEAD if r_i == 0 else CELL
        rows.append([Paragraph(safe(cell.text.strip()), style) for cell in row.cells])
    widths = [7.0 * inch / max(1, len(rows[0]))] * len(rows[0])
    obj = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for idx in range(1, len(rows)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), PALE))
    obj.setStyle(TableStyle(commands))
    return [obj, Spacer(1, 7)]


def body_elements(document):
    bullets = []
    bullet_kind = None

    def flush():
        nonlocal bullets, bullet_kind
        if not bullets:
            return []
        style = "1" if bullet_kind == "List Number" else "bullet"
        result = [ListFlowable([ListItem(Paragraph(safe(x), BODY), leftIndent=9) for x in bullets], bulletType=style, start="1", leftIndent=18, bulletFontSize=8.5, spaceAfter=5)]
        bullets, bullet_kind = [], None
        return result

    result = []
    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            para = DocxParagraph(child, document)
            text = para.text.strip()
            if not text:
                continue
            name = para.style.name
            if name in ("List Bullet", "List Number"):
                if bullet_kind and bullet_kind != name:
                    result.extend(flush())
                bullet_kind = name
                bullets.append(text)
                continue
            result.extend(flush())
            if name == "Title":
                result.append(Paragraph(safe(text), TITLE))
            elif name == "Subtitle":
                result.append(Paragraph(safe(text), SUBTITLE))
            elif name.startswith("Heading"):
                result.append(Paragraph(safe(text), H1))
            elif text.startswith("Evidence boundary"):
                result.append(Paragraph("<b>Evidence boundary</b><br/>" + safe(text.removeprefix("Evidence boundary").strip()), CALLOUT))
            elif is_code(text):
                result.append(Paragraph(safe(text), CODE))
            else:
                result.append(Paragraph(safe(text), BODY))
        elif isinstance(child, CT_Tbl):
            result.extend(flush())
            result.extend(render_table(DocxTable(child, document)))
    result.extend(flush())
    return result


for source in sorted(SOURCE.glob("*.docx")):
    target = OUT / f"{source.stem}.pdf"
    doc = BaseDocTemplate(str(target), pagesize=LETTER, leftMargin=0.72 * inch, rightMargin=0.72 * inch, topMargin=0.66 * inch, bottomMargin=0.76 * inch, title=source.stem)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="review", frames=frame, onPage=page_frame)])
    doc.build(body_elements(Document(source)))
    print(target)
