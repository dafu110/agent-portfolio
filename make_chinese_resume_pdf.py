from pathlib import Path
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "pdf"
ASSETS = ROOT / "assets"
FINAL_PDF = OUT_DIR / "fu-menghan-ai-agent-resume-one-page.pdf"
WEB_RESUME = ASSETS / "resume.pdf"

FONT_REGULAR = "ResumeRegular"
FONT_BOLD = "ResumeBold"

INK = colors.HexColor("#18181B")
TEXT = colors.HexColor("#3F3F46")
MUTED = colors.HexColor("#71717A")
ACCENT = colors.HexColor("#4F46E5")
LINE = colors.HexColor("#D4D4D8")
SOFT = colors.HexColor("#F5F5FA")
WHITE = colors.white


def first_existing(paths):
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("No usable Chinese font found.")


def register_fonts():
    fonts = Path("C:/Windows/Fonts")
    regular = first_existing(
        [fonts / "Deng.ttf", fonts / "msyh.ttc", fonts / "simfang.ttf", fonts / "simsun.ttc"]
    )
    bold = first_existing(
        [fonts / "simhei.ttf", fonts / "msyhbd.ttc", fonts / "Dengb.ttf", fonts / "simsun.ttc"]
    )
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(regular)))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(bold)))


def style(name, **kwargs):
    defaults = {
        "fontName": FONT_REGULAR,
        "fontSize": 9,
        "leading": 12,
        "textColor": TEXT,
        "wordWrap": "CJK",
        "splitLongWords": 1,
        "spaceAfter": 0,
    }
    defaults.update(kwargs)
    return ParagraphStyle(name, **defaults)


def p(text, paragraph_style):
    return Paragraph(text, paragraph_style)


def table_style(*commands):
    return TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            *commands,
        ]
    )


def section(title):
    return [Spacer(1, 6 * mm), p(title, h2), Spacer(1, 2 * mm)]


def bullet(text):
    row = Table([[p("-", bullet_mark), p(text, body)]], colWidths=[4 * mm, CONTENT_W - 4 * mm])
    row.setStyle(table_style(("RIGHTPADDING", (0, 0), (0, 0), 1.5)))
    return row


def project_line(name, value, evidence, link):
    link_text = f'<link href="{link}" color="#4F46E5">查看仓库</link>'
    row = Table(
        [[p(f"<b>{name}</b>", body_bold), p(value, body), p(f"{evidence}<br/>{link_text}", small)]],
        colWidths=[27 * mm, 75 * mm, CONTENT_W - 102 * mm],
    )
    row.setStyle(
        table_style(
            ("LINEBELOW", (0, 0), (-1, 0), 0.35, LINE),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (0, -1), 5),
            ("RIGHTPADDING", (1, 0), (1, -1), 7),
        )
    )
    return row


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 7.5)
    canvas.drawString(15 * mm, 7.5 * mm, "傅孟涵 · AI 应用产品经理 / AI 解决方案顾问")
    canvas.drawRightString(195 * mm, 7.5 * mm, "一页简历 · 2026-07")
    canvas.restoreState()


register_fonts()
OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

PAGE_W, _ = A4
CONTENT_W = PAGE_W - 30 * mm

name_style = style("Name", fontName=FONT_BOLD, fontSize=22, leading=25, textColor=INK)
role_style = style("Role", fontName=FONT_BOLD, fontSize=11, leading=14, textColor=ACCENT)
contact_style = style("Contact", fontSize=9, leading=12, textColor=MUTED)
h2 = style("H2", fontName=FONT_BOLD, fontSize=12.3, leading=15, textColor=ACCENT)
h3 = style("H3", fontName=FONT_BOLD, fontSize=10.8, leading=14, textColor=INK)
body = style("Body", fontSize=10, leading=14.5, textColor=TEXT)
body_bold = style("BodyBold", fontName=FONT_BOLD, fontSize=10, leading=14.5, textColor=INK)
small = style("Small", fontSize=9, leading=12.5, textColor=MUTED)
bullet_mark = style("BulletMark", fontName=FONT_BOLD, fontSize=10, leading=14.5, textColor=ACCENT)

doc = SimpleDocTemplate(
    str(FINAL_PDF),
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=12 * mm,
    bottomMargin=12 * mm,
    title="傅孟涵 - AI 应用产品经理 / AI 解决方案顾问",
    author="傅孟涵",
    subject="一页中文求职简历",
)

portfolio_url = "https://dafu110.github.io/agent-portfolio/"
github_url = "https://github.com/dafu110"
email_url = "mailto:poeticarch@163.com"

header_copy = [
    p("傅孟涵", name_style),
    p("AI 应用产品经理 / AI 解决方案顾问", role_style),
    Spacer(1, 1.5 * mm),
    p(
        "电话 / 微信：15811203776　|　"
        f'<link href="{email_url}" color="#71717A">poeticarch@163.com</link>　|　'
        f'<link href="{github_url}" color="#71717A">GitHub</link><br/>'
        f'<link href="{portfolio_url}" color="#4F46E5">作品集与项目证据室</link>',
        contact_style,
    ),
]
portrait = Image(str(ASSETS / "profile-portrait.jpg"), width=22 * mm, height=27.5 * mm)
header = Table([[header_copy, portrait]], colWidths=[CONTENT_W - 25 * mm, 25 * mm])
header.setStyle(
    table_style(
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    )
)

story = [header, HRFlowable(width="100%", thickness=0.7, color=LINE)]

story.extend(section("个人简介"))
story.append(
    p(
        "10 年建筑设计与复杂项目协同经验，转向企业 AI 应用产品与解决方案。"
        "独立完成 4 个企业工作流原型，覆盖知识检索、工具调用、人工审批、评测与审计。"
        "擅长把模糊需求转化为边界清晰、可验证、可交付的产品方案。",
        body,
    )
)

story.extend(section("工作经历"))
work = Table(
    [[p("2015 至今", body_bold), [p("建筑设计 / 项目负责人", h3), bullet("负责方案设计、跨专业协调、图纸与汇报交付，推进需求澄清、方案评审和关键节点交付。"), bullet("长期处理多方诉求、复杂约束与变更风险，将问题拆解为可执行任务并推动闭环。"), bullet("将十年项目协同经验迁移到 AI 产品工作：明确用户场景、系统边界、验证方式与交付材料。")]]],
    colWidths=[28 * mm, CONTENT_W - 28 * mm],
)
work.setStyle(table_style(("RIGHTPADDING", (0, 0), (0, 0), 6)))
story.append(work)

story.extend(section("AI 项目经历"))
flagship = Table(
    [[
        [p("PeopleOps 智能工作台", h3), p("旗舰项目 · 产品设计 / 原型实现 / 评测", small)],
        [
            p("<b>用户问题：</b>HR 政策问答、候选人处理、审批与审计分散，结论来源和执行责任难以复核。", body),
            p("<b>产品方案：</b>统一知识引用、候选人分析、动作草稿、人工审批和操作记录；高风险动作必须确认后执行。", body),
            p("<b>业务价值：</b>帮助 HR 与业务负责人更快核对信息来源、审批责任和执行状态，降低误操作与返工风险。", body),
            p("<b>验证结果：</b>47 / 47 项单元测试、25 / 25 个离线案例通过；结果仅代表当前原型与样例集。", body),
            p(f'<link href="{github_url}/peopleops-agent" color="#4F46E5">GitHub 仓库</link>　·　<link href="{portfolio_url}#peopleops-demo" color="#4F46E5">90 秒演示</link>', small),
        ],
    ]],
    colWidths=[45 * mm, CONTENT_W - 45 * mm],
)
flagship.setStyle(
    table_style(
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    )
)
story.append(flagship)
story.append(
    project_line(
        "ResearchOps",
        "将研究任务、工具执行、审批与运行状态放进可观察流程。",
        "32 个离线案例覆盖主要路径。",
        f"{github_url}/researchops-agent",
    )
)
story.append(
    project_line(
        "KnowFlow",
        "企业知识检索与引用回答，加入权限过滤、拒答和质量检查。",
        "检索与引用门槛可重复验证。",
        f"{github_url}/knowflow-rag-agent",
    )
)
story.append(
    project_line(
        "Data Analyst",
        "受控查询、字段理解、质量检查与多格式报告导出。",
        "覆盖查询隔离与交付文件生成。",
        f"{github_url}/data-analyst-agent",
    )
)

story.extend(section("专业能力"))
skills = Table(
    [[
        p("<b>产品与方案</b><br/>需求澄清、流程设计、PRD、原型、方案汇报、交付边界", body),
        p("<b>AI 应用</b><br/>RAG、Tool Calling、人工审批、评测回归、审计追踪", body),
        p("<b>工程与 AI 协作</b><br/>Python、FastAPI、Next.js、SQL、Cursor、OpenAI Codex", body),
    ]],
    colWidths=[CONTENT_W / 3] * 3,
)
skills.setStyle(
    table_style(
        ("LINEBEFORE", (1, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (1, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    )
)
story.append(skills)

story.extend(section("教育背景"))
education = Table(
    [[
        p("<b>首都经济贸易大学 × aSSIST University</b><br/>人工智能与大数据工学硕士 · 拟于 2027 年 9 月毕业", body),
        p("<b>内蒙古科技大学</b><br/>建筑学本科 · 2010 - 2015", body),
    ]],
    colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.38],
)
education.setStyle(
    table_style(
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    )
)
story.append(KeepTogether(education))

doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
shutil.copyfile(FINAL_PDF, WEB_RESUME)
print(FINAL_PDF)
print(WEB_RESUME)
