from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.shared import Inches, Pt


ROOT = Path(r"C:\Git\chasewiedemann.github.io")
SOURCE = ROOT / "OTHER" / "ANNUAL REVIEW PROGRESS FORM 2026.docx"
OUTPUT = ROOT / "OTHER" / "ANNUAL REVIEW PROGRESS FORM 2026 - Chase Wiedemann.docx"


def set_run_font(run, size=10.5):
    run.font.name = "Arial"
    run.font.size = Pt(size)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), "Arial")
    rfonts.set(qn("w:hAnsi"), "Arial")


def ensure_response_style(doc):
    name = "Annual Review Response"
    if name in doc.styles:
        return doc.styles[name]
    style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.font.size = Pt(10.5)
    style.paragraph_format.left_indent = Inches(0.55)
    style.paragraph_format.right_indent = Inches(0.05)
    style.paragraph_format.space_before = Pt(2)
    style.paragraph_format.space_after = Pt(7)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    return style


def find_paragraph(doc, exact_text):
    matches = [p for p in doc.paragraphs if p.text.strip() == exact_text]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one paragraph matching {exact_text!r}; found {len(matches)}")
    return matches[0]


def insert_after(anchor, parts, *, indent=0.55, space_after=7):
    new_xml = OxmlElement("w:p")
    anchor._p.addnext(new_xml)
    paragraph = Paragraph(new_xml, anchor._parent)
    paragraph.style = "Annual Review Response"
    paragraph.paragraph_format.left_indent = Inches(indent)
    paragraph.paragraph_format.space_after = Pt(space_after)
    for text, bold, italic in parts:
        run = paragraph.add_run(text)
        run.bold = bold
        run.italic = italic
        set_run_font(run)
    return paragraph


def response(doc, prompt, paragraphs):
    anchor = find_paragraph(doc, prompt)
    for parts in paragraphs:
        anchor = insert_after(anchor, parts)
    return anchor


def answer(text):
    return [("Response: ", True, False), (text, False, False)]


doc = Document(SOURCE)
ensure_response_style(doc)

# Simple identification block, while retaining the original form and directions.
first = doc.paragraphs[0]
meta = first.insert_paragraph_before()
meta.paragraph_format.space_after = Pt(9)
for text, bold in [
    ("Name: ", True),
    ("Chase Wiedemann", False),
    ("  |  Advisor: ", True),
    ("Stephen P. Ryan", False),
]:
    run = meta.add_run(text)
    run.bold = bold
    set_run_font(run, 10.5)

response(
    doc,
    "SCHEDULE A MEETING WITH YOUR ADVISOR",
    [answer("I will meet with Stephen Ryan to review this report and discuss plans for the 2026-2027 year.")],
)

response(
    doc,
    "DRAFT CV",
    [answer("A current CV has been prepared separately.")],
)

response(
    doc,
    "Submit a copy of your Internal Record",
    [answer("My Internal Record will be submitted separately.")],
)

response(
    doc,
    "List any incomplete courses and discuss your plans for completing them.",
    [answer("I have no incomplete courses and have completed my field exams.")],
)

response(
    doc,
    "Dissertation (for students who have passed field exams) - Please summarize progress made on your dissertation research during the past year.  What is your plan for completion? List works currently under review, indicating the current status of the paper.",
    [
        answer(
            "My dissertation is Essays on Local Government Organization. This year I focused mainly on developing and revising my job-market paper on local government centralization and metropolitan growth. I also continued work on a paper with Avinash Sattiraju and a project on local government organization and public-safety policy."
        ),
        [("Current status: ", True, False), ("None of these papers is currently under review.", False, False)],
        [("Plan: ", True, False), ("During 2026-2027 I plan to finish the remaining dissertation chapters, continue revising the job-market paper, and complete the dissertation by May 2027.", False, False)],
    ],
)

response(
    doc,
    "List all new or revised works currently in process (project title, project description, investigator names) and indicate their status.",
    [
        [
            ("Coordination vs. Competition: Local Government Centralization and Metropolitan Growth. ", True, False),
            ("Examines how local government centralization affects metropolitan population and private-employment growth. Investigator: Chase Wiedemann. Status: job-market paper; revised and not under review.", False, False),
        ],
        [
            ("The Organization of Local Government and Economic Dynamism. ", True, False),
            ("Studies the relationship between local government organization and economic dynamism. Investigators: Chase Wiedemann and Avinash Sattiraju. Status: working paper.", False, False),
        ],
        [
            ("Local Government Organization and Endogenous Policy Choice in Public Safety. ", True, False),
            ("Studies how local government organization shapes public-safety policy choices. Investigator: Chase Wiedemann. Status: work in progress.", False, False),
        ],
    ],
)

response(doc, "Research grants applied for or received.", [answer("None.")])
response(doc, "Honors and awards, professional association offices, etc.", [answer("None.")])
response(
    doc,
    "List all professional conferences or symposia which you attended either as a participant and/or presenter. Note whether your work was presented at the conference and, if so, if you presented it.",
    [answer("None during the reporting period.")],
)
response(
    doc,
    "Please indicate your role in organizing and your participation in research activities not included above (e.g. conferences, brown bag workshops, etc.).",
    [answer("No additional organized research activities to report.")],
)

response(
    doc,
    "List all teaching or teaching assistant activities in which you have been involved during the past year and describe your involvement (i.e., activities, amount of time spent, etc.)",
    [
        answer(
            "I served as a teaching assistant for Health Economics in Fall 2025 and Intermediate Microeconomics in Spring 2026. My work mainly involved grading, answering student questions, and helping with course logistics as needed. The time commitment varied by week and was highest around assignments and exams."
        )
    ],
)
response(
    doc,
    "Describe any teaching or teaching assistant activities in which you plan to participate during the coming year.",
    [answer("I plan to serve as a teaching assistant for Econometrics in Fall 2026.")],
)
response(
    doc,
    "Course and other developmental activities you have participated in or plan to enroll for to satisfy the teaching requirements.",
    [answer("I have completed several courses and workshops through the Center for Teaching and Learning and plan to continue participating in relevant CTL programming.")],
)
response(
    doc,
    "Provide your assessment of your overall teaching ability.",
    [answer("I think my teaching ability is solid and continuing to improve. I am comfortable explaining economic concepts and connecting formal material to concrete questions. More classroom experience will help me continue improving pacing and presentation.")],
)

response(
    doc,
    "Any other service, contributions or accomplishments not included above.",
    [answer("I prepared updated materials for the 2026-2027 academic job market, including my CV, teaching statement, research paper, and website. I have no additional service activities to report.")],
)

doc.core_properties.author = "Chase Wiedemann"
doc.core_properties.last_modified_by = "Chase Wiedemann"
doc.core_properties.title = "Annual Review Progress Report 2025-2026"
doc.save(OUTPUT)

# Structural validation: reopen the output and confirm key content and the blank advisor section.
check = Document(OUTPUT)
all_text = "\n".join(p.text for p in check.paragraphs)
required = [
    "Name: Chase Wiedemann  |  Advisor: Stephen P. Ryan",
    "I have no incomplete courses and have completed my field exams.",
    "Coordination vs. Competition: Local Government Centralization and Metropolitan Growth.",
    "I plan to serve as a teaching assistant for Econometrics in Fall 2026.",
    "PHD ADVISOR (Comments)",
]
missing = [item for item in required if item not in all_text]
if missing:
    raise RuntimeError(f"Missing expected content: {missing}")
if not OUTPUT.exists() or OUTPUT.stat().st_size < 10000:
    raise RuntimeError("Output DOCX was not created correctly")

print(OUTPUT)
print(f"Paragraphs: {len(check.paragraphs)}")
print(f"Size: {OUTPUT.stat().st_size} bytes")
