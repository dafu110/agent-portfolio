from pathlib import Path
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "pdf"
ASSETS = ROOT / "assets"
FINAL_PDF = OUT_DIR / "fu-menghan-ai-agent-resume-one-page.pdf"
WEB_RESUME = ASSETS / "resume.pdf"
ROLE_TITLE = "AI Practice Consultant"

INK = colors.HexColor("#18181B")
TEXT = colors.HexColor("#3F3F46")
MUTED = colors.HexColor("#71717A")
ACCENT = colors.HexColor("#4F46E5")
LINE = colors.HexColor("#D4D4D8")
SOFT = colors.HexColor("#F5F5FA")

PAGE_W, _ = A4
CONTENT_W = PAGE_W - 30 * mm
META_W = 29 * mm


def style(name, **kwargs):
    defaults = {
        "fontName": "Helvetica",
        "fontSize": 9,
        "leading": 12,
        "textColor": TEXT,
        "spaceAfter": 0,
    }
    defaults.update(kwargs)
    return ParagraphStyle(name, **defaults)


def p(text, paragraph_style):
    return Paragraph(text, paragraph_style)


def table_style(*commands):
    return TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        *commands,
    ])


def section(title, before=3 * mm, after=1.0 * mm):
    return [Spacer(1, before), p(title, h2), Spacer(1, after)]


def project_line(name, period, value, evidence, link):
    link_text = f'<link href="{link}" color="#4F46E5">Repository</link>'
    row = Table(
        [[
            [
                p(f"<b>{name}</b>", body_bold),
                p(period, small),
                p(link_text, small),
            ],
            [
                p(value, body),
                Spacer(1, 0.8 * mm),
                p(f"<b>Evidence:</b> {evidence}", small),
            ],
        ]],
        colWidths=[META_W, CONTENT_W - META_W],
    )
    row.setStyle(table_style(
        ("LINEBELOW", (0, 0), (-1, 0), 0.35, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (0, -1), 9),
    ))
    return row


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(15 * mm, 7.5 * mm, f"Fu Menghan / {ROLE_TITLE}")
    canvas.drawRightString(195 * mm, 7.5 * mm, "One-page resume / 2026")
    canvas.restoreState()


OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

name_style = style("Name", fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=INK)
role_style = style("Role", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT)
contact_style = style("Contact", fontSize=8.7, leading=10.7, textColor=MUTED)
h2 = style("H2", fontName="Helvetica-Bold", fontSize=12.3, leading=15, textColor=ACCENT)
h3 = style("H3", fontName="Helvetica-Bold", fontSize=10.4, leading=13.5, textColor=INK)
body = style("Body", fontSize=9.7, leading=13.3, textColor=TEXT)
body_bold = style("BodyBold", fontName="Helvetica-Bold", fontSize=9.7, leading=13.3, textColor=INK)
small = style("Small", fontSize=8.6, leading=11.6, textColor=MUTED)
skill_title = style("SkillTitle", fontName="Helvetica-Bold", fontSize=9.2, leading=11.8, textColor=ACCENT)
skill_body = style("SkillBody", fontSize=8.7, leading=11.5, textColor=TEXT)
work_meta = style("WorkMeta", fontSize=8.7, leading=11.5, textColor=MUTED)
work_role = style("WorkRole", fontName="Helvetica-Bold", fontSize=8.8, leading=11.3, textColor=ACCENT)
work_scope = style("WorkScope", fontSize=8.9, leading=12.0, textColor=MUTED)

portfolio_url = "https://dafu110.github.io/agent-portfolio/"
github_url = "https://github.com/dafu110"
email_url = "mailto:poeticarch@163.com"

header_copy = [
    p("Fu Menghan", name_style),
    p(ROLE_TITLE, role_style),
    Spacer(1, 1 * mm),
    p(
        "Beijing / available to work in Beijing / available now / on-site, hybrid or remote<br/>"
        "Phone and WeChat: 15811203776 | "
        f'<link href="{email_url}" color="#71717A">poeticarch@163.com</link> | '
        f'<link href="{github_url}" color="#71717A">GitHub</link><br/>'
        f'Portfolio: <link href="{portfolio_url}" color="#4F46E5">{portfolio_url}</link>',
        contact_style,
    ),
]
portrait = Image(str(ASSETS / "profile-portrait.png"), width=26 * mm, height=32.5 * mm)
portrait.hAlign = "RIGHT"
header = Table([[header_copy, portrait]], colWidths=[CONTENT_W - 30 * mm, 30 * mm])
header.setStyle(table_style(
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (0, 0), 12),
    ("LEFTPADDING", (1, 0), (1, 0), 5),
))

story = [header, HRFlowable(width="100%", thickness=0.7, color=LINE)]

story.extend(section("Profile summary", before=3.5 * mm, after=1.3 * mm))
story.append(p(
    "AI Practice Consultant for practical, people-facing AI adoption. I connect 10 years of architecture and project delivery with hands-on AI prototyping: identifying useful opportunities across design, workplace strategy, engineering, delivery and operations; building lightweight demos, prompts, prototypes and tools; explaining them clearly; and packaging reusable guidance for colleague trials.",
    body,
))

story.extend(section("Role-fit capabilities", before=3.8 * mm, after=1.2 * mm))
skills = Table(
    [[
        [p("Opportunity Discovery", skill_title), p("Use-case mapping, problem framing, pilot scope and non-goal definition.", skill_body)],
        [p("Workflow Prototyping", skill_title), p("Lightweight prompts, TaskSpecs, demos, prototypes and practical tools.", skill_body)],
        [p("Enablement & Scaling", skill_title), p("Colleague support, clear AI explanation, guidance, playbooks and evaluation notes.", skill_body)],
    ]],
    colWidths=[CONTENT_W / 3] * 3,
)
skills.setStyle(table_style(
    ("LINEABOVE", (0, 0), (-1, 0), 0.9, ACCENT),
    ("RIGHTPADDING", (0, 0), (-2, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
))
story.append(skills)

story.extend(section("AI project experience", before=4.0 * mm, after=1.0 * mm))
story.append(project_line(
    "ArchMind",
    "2026.08 / flagship",
    "Architecture AI Practice Workspace demo that turns SU screenshots, structured prompts, design review and team templates into a reusable AI practice example.",
    "4 SU-to-render cases; TaskSpec; demo video; toolkit for colleague trials.",
    f"{github_url}/Architecture-AI-Practice-Workspace",
))
story.append(project_line(
    "BuildLoop AI",
    "2026.08",
    "Construction early-warning loop connecting drawings, BIM, standards, meetings, messages and site reports into reviewable alerts.",
    "283 tests passed; evaluation covers evidence location, risk level and approval drafts.",
    f"{github_url}/BuildLoop-Al",
))
story.append(project_line(
    "PeopleOps",
    "2026.07",
    "Traceable HR workflow connecting policy evidence, candidate actions, human approval and audit records.",
    "47 / 47 unit tests; 25 / 25 offline cases; source-grounded actions with approval before execution.",
    f"{github_url}/peopleops-intelligence-agent",
))

story.extend(section("Work experience", before=4.0 * mm, after=1.0 * mm))
work = Table(
    [
        [p("2023 - present", work_meta), [p("North China Municipal Engineering Design & Research Institute", body_bold), p("Project lead", work_role), p("Public buildings and municipal supporting projects; requirement discovery, cross-discipline coordination and client reporting.", work_scope)]],
        [p("2017 - 2023", work_meta), [p("Beijing Turenscape Urban Planning & Design Co., Ltd. / Beijing Institute of Architectural Design Co., Ltd.", body_bold), p("Project lead", work_role), p("Cultural tourism, industrial parks, education and public-service projects; scheme development, client communication and review delivery.", work_scope)]],
        [p("2015 - 2017", work_meta), [p("Beijing Chuangyan Architecture Design Center", body_bold), p("Assistant architect", work_role), p("Concept design and scheme refinement for campus, transportation and medical industrial park projects.", work_scope)]],
    ],
    colWidths=[META_W, CONTENT_W - META_W],
)
work.setStyle(table_style(
    ("LINEBELOW", (0, 0), (-1, -2), 0.35, LINE),
    ("TOPPADDING", (0, 0), (-1, -1), 4.2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
    ("RIGHTPADDING", (0, 0), (0, -1), 9),
))
story.append(work)

representative = Table(
    [[
        p("Representative delivery", small),
        p("<b>Qihe National Modern Agriculture Industrial Park Integrated Service Center</b> / 52,500 sqm site, 29,000 sqm GFA, 103.8 m ring structure; <b>Yueqing Yanshan summit building proposal</b> / 3,657 sqm, first-prize scheme, long-span timber structure.", small),
    ]],
    colWidths=[34 * mm, CONTENT_W - 34 * mm],
)
representative.setStyle(table_style(
    ("LINEBEFORE", (0, 0), (0, 0), 1.2, ACCENT),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ("LEFTPADDING", (0, 0), (0, 0), 5),
    ("LEFTPADDING", (1, 0), (1, 0), 2),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
))
story.append(Spacer(1, 1.4 * mm))
story.append(representative)

story.extend(section("Education", before=3.8 * mm, after=1.0 * mm))
education = Table(
    [[
        p("<b>Capital University of Economics and Business x aSSIST University</b><br/>M.S. in AI and Big Data Engineering / expected September 2027", body),
        p("<b>Inner Mongolia University of Science & Technology</b><br/>B.Arch. / 2010 - 2015", body),
    ]],
    colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.38],
)
education.setStyle(table_style(
    ("LINEABOVE", (0, 0), (-1, 0), 0.9, ACCENT),
    ("RIGHTPADDING", (0, 0), (0, 0), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
))
story.append(education)


doc = SimpleDocTemplate(
    str(FINAL_PDF),
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=8 * mm,
    bottomMargin=9 * mm,
    title=f"Fu Menghan - {ROLE_TITLE}",
    author="Fu Menghan",
    subject="One-page resume",
)
doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
shutil.copyfile(FINAL_PDF, WEB_RESUME)
print(FINAL_PDF)
print(WEB_RESUME)
