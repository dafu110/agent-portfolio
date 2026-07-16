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


def section(title, before=3.3 * mm, after=1 * mm):
    return [Spacer(1, before), p(title, h2), Spacer(1, after)]


def bullet(text):
    row = Table([[p("-", bullet_mark), p(text, body)]], colWidths=[4 * mm, CONTENT_W - 4 * mm])
    row.setStyle(table_style(("RIGHTPADDING", (0, 0), (0, 0), 1.5)))
    return row


def project_line(name, period, value, evidence, link):
    link_text = f'<link href="{link}" color="#4F46E5">查看仓库</link>'
    row = Table(
        [[
            [p(f"<b>{name}</b>", body_bold), p(period, small)],
            p(value, body),
            p(f"{evidence}<br/>{link_text}", small),
        ]],
        colWidths=[27 * mm, 75 * mm, CONTENT_W - 102 * mm],
    )
    row.setStyle(
        table_style(
            ("LINEBELOW", (0, 0), (-1, 0), 0.35, LINE),
            ("TOPPADDING", (0, 0), (-1, -1), 4.8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.8),
            ("RIGHTPADDING", (0, 0), (0, -1), 5),
            ("RIGHTPADDING", (1, 0), (1, -1), 7),
        )
    )
    return row


def career_line(period, employer, role, scope):
    return [
        p(period, work_meta),
        [p(f"<b>{employer}</b>", work_employer), p(role, work_meta)],
        p(scope, work_scope),
    ]


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
contact_style = style("Contact", fontSize=8.8, leading=10.2, textColor=MUTED)
h2 = style("H2", fontName=FONT_BOLD, fontSize=12.3, leading=15, textColor=ACCENT)
h3 = style("H3", fontName=FONT_BOLD, fontSize=10.8, leading=14, textColor=INK)
body = style("Body", fontSize=10, leading=14.5, textColor=TEXT)
body_bold = style("BodyBold", fontName=FONT_BOLD, fontSize=10, leading=14.5, textColor=INK)
small = style("Small", fontSize=9, leading=12.5, textColor=MUTED)
bullet_mark = style("BulletMark", fontName=FONT_BOLD, fontSize=10, leading=14.5, textColor=ACCENT)
flagship_body = style("FlagshipBody", fontSize=10, leading=14.7, textColor=TEXT, spaceAfter=1.3)
work_employer = style("WorkEmployer", fontName=FONT_BOLD, fontSize=9.3, leading=11.5, textColor=INK)
work_meta = style("WorkMeta", fontSize=8.6, leading=11.3, textColor=MUTED)
work_scope = style("WorkScope", fontSize=8.8, leading=11.8, textColor=MUTED)
scheme_label = style("SchemeLabel", fontSize=8.4, leading=11, textColor=MUTED)
scheme_text = style("SchemeText", fontSize=8.7, leading=11.7, textColor=MUTED)

doc = SimpleDocTemplate(
    str(FINAL_PDF),
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=10 * mm,
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
    Spacer(1, 1.0 * mm),
    p(
        "北京 · 可在北京工作 · 随时到岗 · 现场 / 混合 / 远程均可<br/>"
        "电话 / 微信：15811203776　|　"
        f'<link href="{email_url}" color="#71717A">poeticarch@163.com</link>　|　'
        f'<link href="{github_url}" color="#71717A">GitHub</link><br/>'
        f'作品集：<link href="{portfolio_url}" color="#4F46E5">{portfolio_url}</link>',
        contact_style,
    ),
]
portrait = Image(str(ASSETS / "profile-portrait.png"), width=20 * mm, height=25 * mm)
header = Table([[header_copy, portrait]], colWidths=[CONTENT_W - 25 * mm, 25 * mm])
header.setStyle(
    table_style(
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    )
)

story = [header, HRFlowable(width="100%", thickness=0.7, color=LINE)]

story.extend(section("个人简介", after=1.25 * mm))
story.append(
    p(
        "聚焦企业 AI 应用产品与解决方案，已独立完成 4 个可验证工作流原型，"
        "覆盖 RAG、工具调用、人工审批、评测与审计；叠加 10 年复杂项目协同与方案交付经验，"
        "擅长把模糊需求转化为边界清晰、可验证的产品方案。",
        body,
    )
)

work = Table(
    [
        career_line(
            "2023 - 至今",
            "中国市政工程华北设计研究总院",
            "项目负责人",
            "公共建筑与市政配套；负责方案深化、跨专业协调与甲方汇报。",
        ),
        career_line(
            "2017 - 2019、2021 - 2023",
            "北京土人城市规划设计股份有限公司",
            "项目负责人",
            "文旅、产业园与公共服务项目的规划及建筑方案。",
        ),
        career_line(
            "2019 - 2021",
            "北京市建筑设计研究院股份有限公司",
            "项目负责人",
            "教育建筑与改造项目；推进方案、客户沟通与评审交付。",
        ),
        career_line(
            "2015 - 2017",
            "北京创研建筑设计中心",
            "助理建筑师",
            "参与校园、交通与医疗产业园的概念设计和方案深化。",
        ),
    ],
    colWidths=[38 * mm, 54 * mm, CONTENT_W - 92 * mm],
)
work.setStyle(
    table_style(
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 3.7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.7),
        ("RIGHTPADDING", (0, 0), (1, -1), 5.5),
    )
)
representative_schemes = Table(
    [
        [
            p("代表方案 01", scheme_label),
            p(
                "<b>齐河县国家现代农业产业园综合服务中心</b> · 占地 5.25 万㎡ / 建筑面积 2.9 万㎡ / "
                "环形结构外径 103.8 米；整合展馆、检测、研发、仓储与研学。",
                scheme_text,
            ),
        ],
        [
            p("代表方案 02", scheme_label),
            p(
                "<b>乐清市盐盆山清和公园一体化建设工程 - 山顶建筑设计方案</b> · "
                "3657㎡ · 方案设计一等奖；大跨度木结构串联观景、休憩与冥想。",
                scheme_text,
            ),
        ],
    ],
    colWidths=[26 * mm, CONTENT_W - 26 * mm],
)
representative_schemes.setStyle(
    table_style(
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.35, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
    )
)
story.extend(section("AI 项目经历", before=4.8 * mm, after=1.8 * mm))
flagship = Table(
    [[
        [p("PeopleOps 智能工作台", h3), p("2026.07 · 旗舰项目<br/>产品设计 / 原型实现 / 评测", small)],
        [
            p("<b>方案：</b>政策证据、候选人动作与审批进入同一工作流；高风险动作须人工确认。", flagship_body),
            p("<b>价值：</b>更快核对来源、责任与状态，降低误操作和返工风险。", flagship_body),
            p("<b>验证：</b>47 / 47 项测试、25 / 25 个离线案例通过；仅代表当前原型与样例集。", flagship_body),
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
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    )
)
story.append(flagship)
story.append(
    project_line(
        "ResearchOps",
        "2026.07",
        "将研究任务、工具执行、审批与运行状态放进可观察流程。",
        "32 个离线案例覆盖主要路径。",
        f"{github_url}/researchops-agent",
    )
)
story.append(
    project_line(
        "KnowFlow",
        "2026.07",
        "企业知识检索与引用回答，加入权限过滤、拒答和质量检查。",
        "检索与引用门槛可重复验证。",
        f"{github_url}/knowflow-rag-agent",
    )
)
story.append(
    project_line(
        "Data Analyst",
        "2026.07",
        "受控查询、字段理解、质量检查与多格式报告导出。",
        "覆盖查询隔离与交付文件生成。",
        f"{github_url}/data-analyst-agent",
    )
)

story.extend(section("工作经历", before=5.0 * mm, after=1.6 * mm))
story.append(work)
story.append(representative_schemes)

story.extend(section("专业能力", before=5.4 * mm, after=1.4 * mm))
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
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.45, LINE),
        ("LINEBEFORE", (1, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.6),
    )
)
story.append(skills)

story.extend(section("教育背景", before=5.6 * mm, after=1.2 * mm))
education = Table(
    [[
        p("<b>首都经济贸易大学 × aSSIST University</b><br/>人工智能与大数据工学硕士 · 拟于 2027 年 9 月毕业", body),
        p("<b>内蒙古科技大学</b><br/>建筑学本科 · 2010 - 2015", body),
    ]],
    colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.38],
)
education.setStyle(
    table_style(
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.45, LINE),
        ("LINEBEFORE", (1, 0), (1, 0), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6.0),
    )
)
story.append(KeepTogether(education))

doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
shutil.copyfile(FINAL_PDF, WEB_RESUME)
print(FINAL_PDF)
print(WEB_RESUME)
