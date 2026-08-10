"""Build the public CV PDF from the Markdown source in cv.md."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cv.md"
OUTPUT = ROOT / "files" / "Chase_Wiedemann_CV.pdf"
LOGO = ROOT / "assets" / "images" / "washu-olin-logo.png"

INK = colors.HexColor("#263238")
MUTED = colors.HexColor("#65727A")
ACCENT = colors.HexColor("#2F7F99")
RULE = colors.HexColor("#D9E0E3")
CONTENT_WIDTH = 7.40 * inch


def register_fonts() -> tuple[str, str, str, str]:
    """Prefer bundled Windows fonts, with portable PDF core-font fallbacks."""
    candidates = [
        (
            Path("C:/Windows/Fonts/cambria.ttc"),
            Path("C:/Windows/Fonts/cambriab.ttf"),
            Path("C:/Windows/Fonts/cambriai.ttf"),
            Path("C:/Windows/Fonts/cambriaz.ttf"),
        ),
        (
            Path("C:/Windows/Fonts/georgia.ttf"),
            Path("C:/Windows/Fonts/georgiab.ttf"),
            Path("C:/Windows/Fonts/georgiai.ttf"),
            Path("C:/Windows/Fonts/georgiaz.ttf"),
        ),
    ]
    for regular, bold, italic, bold_italic in candidates:
        if all(path.exists() and path.suffix.lower() == ".ttf" for path in (regular, bold, italic, bold_italic)):
            pdfmetrics.registerFont(TTFont("CVSerif", str(regular)))
            pdfmetrics.registerFont(TTFont("CVSerif-Bold", str(bold)))
            pdfmetrics.registerFont(TTFont("CVSerif-Italic", str(italic)))
            pdfmetrics.registerFont(TTFont("CVSerif-BoldItalic", str(bold_italic)))
            pdfmetrics.registerFontFamily(
                "CVSerif",
                normal="CVSerif",
                bold="CVSerif-Bold",
                italic="CVSerif-Italic",
                boldItalic="CVSerif-BoldItalic",
            )
            return "CVSerif", "CVSerif-Bold", "CVSerif-Italic", "CVSerif-BoldItalic"
    return "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"


BODY_FONT, BOLD_FONT, ITALIC_FONT, BOLD_ITALIC_FONT = register_fonts()


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def clean_inline(text: str) -> str:
    placeholders: dict[str, str] = {}

    def hold(value: str) -> str:
        key = f"@@HTML{len(placeholders)}@@"
        placeholders[key] = value
        return key

    text = re.sub(r"<br\s*/?>", lambda _: hold("<br/>"), text, flags=re.I)
    text = re.sub(
        r'<a\s+href="([^"]+)">(.+?)</a>',
        lambda m: hold(f'<link href="{html.escape(m.group(1), quote=True)}">{html.escape(m.group(2))}</link>'),
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\[([^]]+)\]\(([^)]+)\)",
        lambda m: hold(f'<link href="{html.escape(m.group(2), quote=True)}">{html.escape(m.group(1))}</link>'),
        text,
    )
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(.+?)\*(?!\*)", r"<i>\1</i>", text)
    text = text.replace("  ", " ")
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.47 * inch, LETTER[0] - doc.rightMargin, 0.47 * inch)
    canvas.setFont(BODY_FONT, 7.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.31 * inch, "Chase Wiedemann - Curriculum Vitae - Updated August 2026")
    canvas.drawRightString(LETTER[0] - doc.rightMargin, 0.31 * inch, str(doc.page))
    canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "CVName",
            parent=base["Title"],
            fontName=BOLD_FONT,
            fontSize=20,
            leading=22,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=2,
        ),
        "tagline": ParagraphStyle(
            "CVTagline",
            parent=base["Normal"],
            fontName=BOLD_FONT,
            fontSize=8.6,
            leading=9.6,
            alignment=TA_CENTER,
            textColor=ACCENT,
            spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "CVContact",
            parent=base["Normal"],
            fontName=BODY_FONT,
            fontSize=7.7,
            leading=9.4,
            alignment=TA_CENTER,
            textColor=MUTED,
            linkColor=ACCENT,
            spaceAfter=3,
        ),
        "section": ParagraphStyle(
            "CVSection",
            parent=base["Heading2"],
            fontName=BOLD_FONT,
            fontSize=9.15,
            leading=10.4,
            textColor=ACCENT,
            spaceBefore=4,
            spaceAfter=2,
            keepWithNext=True,
            borderWidth=0,
        ),
        "subsection": ParagraphStyle(
            "CVSubsection",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=7.4,
            leading=8.7,
            textColor=ACCENT,
            spaceBefore=2,
            spaceAfter=1,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "CVBody",
            parent=base["BodyText"],
            fontName=BODY_FONT,
            fontSize=7.75,
            leading=9.35,
            textColor=INK,
            spaceAfter=2.8,
            linkColor=ACCENT,
        ),
        "cell": ParagraphStyle(
            "CVCell",
            parent=base["BodyText"],
            fontName=BODY_FONT,
            fontSize=7.35,
            leading=8.65,
            textColor=INK,
            linkColor=ACCENT,
        ),
        "date": ParagraphStyle(
            "CVDate",
            parent=base["BodyText"],
            fontName=ITALIC_FONT,
            fontSize=7.0,
            leading=8.2,
            alignment=TA_RIGHT,
            textColor=MUTED,
        ),
        "reference": ParagraphStyle(
            "CVReference",
            parent=base["BodyText"],
            fontName=BODY_FONT,
            fontSize=6.9,
            leading=8.1,
            textColor=INK,
            linkColor=ACCENT,
        ),
        "updated": ParagraphStyle(
            "CVUpdated",
            parent=base["BodyText"],
            fontName=ITALIC_FONT,
            fontSize=6.8,
            alignment=TA_RIGHT,
            textColor=MUTED,
            spaceBefore=5,
        ),
    }


def build_story(markdown_text: str):
    styles = make_styles()
    lines = strip_front_matter(markdown_text).splitlines()
    story = []
    current_section = ""
    i = 0

    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line:
            i += 1
            continue

        if line.startswith("# "):
            story.append(Paragraph(clean_inline(line[2:].strip()), styles["name"]))
            i += 1
            continue

        if line.startswith('<p class="cv-logo">'):
            logo_width = 2.65 * inch
            logo = Image(str(LOGO), width=logo_width, height=logo_width * 119 / 1024)
            logo.hAlign = "CENTER"
            story.append(logo)
            story.append(Spacer(1, 5))
            i += 1
            continue

        if line.startswith('<p class="cv-tagline">'):
            inner = re.sub(r"^<p[^>]*>|</p>$", "", line)
            story.append(Paragraph(inner, styles["tagline"]))
            i += 1
            continue

        if line.startswith('<p class="cv-contact">'):
            inner = re.sub(r"^<p[^>]*>|</p>$", "", line)
            inner = re.sub(r"<br\s*>", "<br/>", inner, flags=re.I)
            story.append(Paragraph(inner.replace("&middot;", "&#183;"), styles["contact"]))
            story.append(Spacer(1, 1))
            i += 1
            continue

        if line.startswith('<p class="cv-actions">'):
            i += 1
            continue

        if line.startswith('<p class="cv-updated">'):
            i += 1
            continue

        if line.startswith("## "):
            current_section = line[3:].strip()
            heading = Paragraph(clean_inline(current_section.upper()), styles["section"])
            rule = Table([[heading]], colWidths=[CONTENT_WIDTH])
            rule.setStyle(
                TableStyle(
                    [
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.65, RULE),
                    ]
                )
            )
            story.append(rule)
            i += 1
            continue

        if line.startswith("### "):
            story.append(Paragraph(clean_inline(line[4:].strip()), styles["subsection"]))
            i += 1
            continue

        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            parsed = [split_table_row(value) for value in table_lines if not is_table_separator(value)]
            if parsed:
                parsed = parsed[1:]  # Markdown header row is intentionally blank.
            if not parsed:
                continue

            if current_section == "References":
                data = [
                    [Paragraph(clean_inline(cell), styles["reference"]) for cell in row]
                    for row in parsed
                ]
                table = Table(data, colWidths=[3.64 * inch, 3.64 * inch], hAlign="LEFT")
                commands = [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
                table.setStyle(TableStyle(commands))
            else:
                data = []
                for row in parsed:
                    left = Paragraph(clean_inline(row[0]), styles["cell"])
                    right = Paragraph(clean_inline(row[1]), styles["date"])
                    data.append([left, right])
                table = Table(data, colWidths=[6.05 * inch, 1.23 * inch], hAlign="LEFT")
                table.setStyle(
                    TableStyle(
                        [
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (0, -1), 10),
                            ("RIGHTPADDING", (1, 0), (1, -1), 0),
                            ("TOPPADDING", (0, 0), (-1, -1), 1),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ]
                    )
                )
            story.append(table)
            continue

        if line.startswith("- "):
            while i < len(lines) and lines[i].strip().startswith("- "):
                item = lines[i].strip()[2:].strip()
                story.append(Paragraph(f"&#8226;&nbsp;&nbsp;{clean_inline(item)}", styles["body"]))
                i += 1
            continue

        paragraph_lines = [line]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate or candidate.startswith(("#", "|", "- ", "<p class=")):
                break
            paragraph_lines.append(candidate)
            i += 1
        joined = " ".join(paragraph_lines)
        story.append(Paragraph(clean_inline(joined), styles["body"]))

    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = LETTER
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=LETTER,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.40 * inch,
        bottomMargin=0.53 * inch,
        title="Chase Wiedemann - Curriculum Vitae",
        author="Chase Wiedemann",
        subject="Academic curriculum vitae",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        page_width - doc.leftMargin - doc.rightMargin,
        page_height - doc.topMargin - doc.bottomMargin,
        id="cv",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="CV", frames=[frame], onPage=footer)])
    doc.build(build_story(SOURCE.read_text(encoding="utf-8")))
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
