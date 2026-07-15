from pathlib import Path
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, TableStyle


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "pdf"
ASSETS = ROOT / "assets"
FINAL_PDF = OUT_DIR / "fu-menghan-ai-agent-resume-one-page.pdf"
WEB_RESUME = ASSETS / "resume.pdf"

FONT_REGULAR = "ResumeRegular"
FONT_BOLD = "ResumeBold"

INK = colors.HexColor("#18181b")
TEXT = colors.HexColor("#3f3f46")
MUTED = colors.HexColor("#71717a")
ACCENT = colors.HexColor("#4f46e5")
LINE = colors.HexColor("#d4d4d8")
SOFT = colors.HexColor("#f7f7f8")
WHITE = colors.white


def first_existing(paths):
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("No usable Chinese font found.")


def register_fonts() -> None:
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
    base = {
        "fontName": FONT_REGULAR,
        "fontSize": 7.4,
        "leading": 9.3,
        "textColor": TEXT,
        "wordWrap": "CJK",
        "splitLongWords": 1,
        "spaceAfter": 0,
    }
    base.update(kwargs)
    return ParagraphStyle(name, **base)


def p(text, sty):
    return Paragraph(text, sty)


def table_style(commands):
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


def boxed(content, width, background=WHITE, pad=4.5, stroke=LINE):
    table = Table([[content]], colWidths=[width])
    table.setStyle(
        table_style(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.45, stroke),
                ("LEFTPADDING", (0, 0), (-1, -1), pad),
                ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                ("TOPPADDING", (0, 0), (-1, -1), pad),
                ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
            ]
        )
    )
    return table


def bullets(items, width):
    rows = [[p("-", bullet_style), p(item, small)] for item in items]
    table = Table(rows, colWidths=[3.6 * mm, width - 3.6 * mm])
    table.setStyle(
        table_style(
            [
                ("RIGHTPADDING", (0, 0), (0, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1),
            ]
        )
    )
    return table


def metric(value, label):
    return [p(value, metric_value), p(label, tiny)]


def project_row(title, focus, proof, repo):
    return [
        p(f"<b>{title}</b><br/>{focus}", small),
        p(f"{proof}<br/><font color='#71717a'>{repo}</font>", tiny),
    ]


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 6.3)
    canvas.drawString(10 * mm, 7 * mm, "傅孟涵 - AI 应用产品经理 / AI 解决方案顾问")
    canvas.drawRightString(200 * mm, 7 * mm, "poeticarch@163.com | 15811203776")
    canvas.restoreState()


register_fonts()
OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

name_style = style("Name", fontName=FONT_BOLD, fontSize=22, leading=23.5, textColor=INK)
role_style = style("Role", fontName=FONT_BOLD, fontSize=10.5, leading=12, textColor=ACCENT)
contact_style = style("Contact", fontSize=7.2, leading=8.6, textColor=MUTED)
h2 = style("H2", fontName=FONT_BOLD, fontSize=9.8, leading=11.2, textColor=ACCENT)
h3 = style("H3", fontName=FONT_BOLD, fontSize=8.6, leading=10, textColor=INK)
body = style("Body", fontSize=7.35, leading=9.35, textColor=TEXT)
small = style("Small", fontSize=6.95, leading=8.7, textColor=TEXT)
tiny = style("Tiny", fontSize=6.25, leading=7.7, textColor=MUTED)
bullet_style = style("Bullet", fontName=FONT_BOLD, fontSize=6.9, leading=8.6, textColor=ACCENT)
metric_value = style("MetricValue", fontName=FONT_BOLD, fontSize=11.2, leading=12.2, textColor=INK)

doc = SimpleDocTemplate(
    str(FINAL_PDF),
    pagesize=A4,
    rightMargin=10 * mm,
    leftMargin=10 * mm,
    topMargin=8.5 * mm,
    bottomMargin=10 * mm,
    title="傅孟涵 AI 应用产品经理、AI 解决方案顾问一页简历",
    author="傅孟涵",
)

story = []

portrait = Image(str(ASSETS / "profile-portrait.jpg"), width=22 * mm, height=27.5 * mm)
header_left = [
    p("傅孟涵", name_style),
    p("AI 应用产品经理、AI 解决方案顾问", role_style),
    p(
        "电话 / 微信：15811203776  |  邮箱：poeticarch@163.com  |  GitHub：github.com/dafu110<br/>"
        "作品集：https://dafu110.github.io/agent-portfolio/",
        contact_style,
    ),
]
header = Table([[header_left, portrait]], colWidths=[156 * mm, 24 * mm])
header.setStyle(
    table_style(
        [
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.6, LINE),
        ]
    )
)
story.append(header)

left_w = 42 * mm
right_col_w = 138 * mm
right_w = right_col_w - 7 * mm
layout_h = 232 * mm

sidebar = Table(
    [
        [p("求职定位", h2)],
        [p("AI 应用产品经理<br/>AI 解决方案顾问<br/>企业 Agent / RAG 方向", body)],
        [p("核心能力", h2)],
        [
            bullets(
                [
                    "Agent 工作流设计",
                    "RAG 与知识可信",
                    "工具调用治理",
                    "人工审批与审计",
                    "评测门禁与回归",
                    "复杂需求拆解",
                ],
                left_w - 10 * mm,
            )
        ],
        [p("工具与技术", h2)],
        [
            p(
                "<b>AI / Agent</b><br/>RAG、Tool Calling、Planner、Trace、HITL、Eval Gate<br/><br/>"
                "<b>工程实现</b><br/>Python、FastAPI、Next.js、SQL、Chroma、BM25 / TF-IDF<br/><br/>"
                "<b>交付表达</b><br/>PRD、流程图、测试用例、界面原型、方案汇报",
                body,
            )
        ],
        [p("教育背景", h2)],
        [
            p(
                "<b>内蒙古科技大学</b><br/>建筑学本科<br/>2010 - 2015<br/><br/>"
                "<b>首都经济贸易大学 x aSSIST University</b><br/>人工智能与大数据工学硕士<br/>拟于 2027 年 9 月毕业",
                body,
            )
        ],
        [p("作品材料", h2)],
        [p("网页作品集：首页<br/>项目证据室：cases 页面<br/>PDF：一页中文简历<br/>GitHub：dafu110", body)],
    ],
    colWidths=[left_w - 10 * mm],
    rowHeights=[7 * mm, 24 * mm, 7 * mm, 37 * mm, 7 * mm, 53 * mm, 7 * mm, 41 * mm, 7 * mm, 31 * mm],
)
sidebar.setStyle(table_style([]))

summary = (
    "10 年建筑设计与复杂项目协同经验，转向企业 AI 应用产品与解决方案。"
    "已独立完成 4 个面向企业工作流的 AI 应用原型，覆盖 RAG、工具调用、审批治理、评测门禁、审计日志和产品化交付。"
    "核心优势是把模糊业务需求拆成可评审、可治理、可复核的系统方案。"
)

metrics = Table(
    [[metric("10 年", "复杂项目协同"), metric("4 个", "AI 应用原型"), metric("47 / 47", "PeopleOps 单元测试"), metric("25 / 25", "PeopleOps 离线案例")]],
    colWidths=[right_w / 4] * 4,
)
metrics.setStyle(
    table_style(
        [
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
        ]
    )
)

work_table = Table(
    [
        [
            p("2015 至今<br/><b>建筑设计 / 项目负责人</b>", small),
            p("负责方案设计、跨专业接口协调、图纸与汇报交付；持续处理需求变化、设计约束与交付节点，形成需求澄清、方案评审和多方协同能力。", small),
        ],
        [
            p("2025 - 2026<br/><b>个人 AI 应用项目实践</b>", small),
            p("围绕企业工作流、RAG、研究流程和数据分析，独立完成问题定义、原型实现、测试评测与证据整理；均为本地样例集原型。", small),
        ],
    ],
    colWidths=[33 * mm, right_w - 33 * mm],
)
work_table.setStyle(
    table_style(
        [
            ("BACKGROUND", (0, 0), (-1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4.2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ]
    )
)

flagship = boxed(
    [
        p("PeopleOps 智能工作台", h3),
        p(
            "<b>定位：</b>不是 HR 聊天机器人，而是把政策回答、候选人动作、人工审批与审计放进同一条链路的 Agent 工作台。",
            small,
        ),
        p(
            "<b>关键设计：</b>候选人分析只输出带来源证据，不给录用结论；外部动作从草稿开始，显式提交并审批后执行。",
            small,
        ),
        p(
            "<b>可复核证据：</b>2026-07-13，47 / 47 单元测试、25 / 25 离线案例通过；含 10 条黄金轨迹、10 条 RAG fixture、5 条候选人安全案例。",
            small,
        ),
        p("<b>边界：</b>本地确定性 fixture 与安全回归，不代表真实用户效果或线上模型质量。", tiny),
    ],
    right_w,
    SOFT,
    pad=5,
)

project_index = Table(
    [
        project_row(
            "ResearchOps",
            "可观察、可审批、可复核的研究流程 Agent。",
            "pytest 覆盖任务队列、工具注册和运行状态；32 条离线评测案例。",
            "github.com/dafu110/researchops-agent",
        ),
        project_row(
            "KnowFlow",
            "企业知识检索、引用回答、权限过滤与拒答的 RAG 原型。",
            "主评测集与 holdout 的 Recall@k、引用准确性等门槛均为 >= 0.95。",
            "github.com/dafu110/knowflow-rag-agent",
        ),
        project_row(
            "Data Analyst",
            "受控查询、字段理解、质量检查与报告导出的数据分析 Agent。",
            "可复核字段识别、隔离执行及 Markdown / HTML / CSV / PDF / PPTX 输出路径。",
            "github.com/dafu110/data-analyst-agent",
        ),
    ],
    colWidths=[45 * mm, right_w - 45 * mm],
)
project_index.setStyle(
    table_style(
        [
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)

match_table = Table(
    [
        [
            p("<b>可承担</b><br/>售前方案、产品原型、需求澄清、Demo 设计、评测方案、交付材料。", small),
            p("<b>当前重点</b><br/>企业 Agent 工作流、知识库可信回答、工具调用治理和可复核界面。", small),
            p("<b>项目边界</b><br/>指标描述当前实现和样例集，不等同真实线上业务成效。", small),
        ]
    ],
    colWidths=[right_w / 3] * 3,
)
match_table.setStyle(
    table_style(
        [
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)

background_box = boxed(
    [
        p(
            "建筑项目训练我处理模糊需求、多方角色、复杂约束和交付边界，可迁移到企业 AI 项目的需求澄清、方案设计、客户沟通和落地推进。",
            small,
        ),
        p(
            "相对纯技术候选人，我更关注系统是否能被复核：任务如何定义，结果如何验证，权限如何治理，风险如何控制。",
            small,
        ),
    ],
    right_w,
    WHITE,
    pad=6.5,
)

verify_path = Table(
    [
        [
            p("<b>读边界</b><br/>先看 README、使用对象、运行方式和明确不做什么。", small),
            p("<b>读证据</b><br/>检查 tests、evals、黄金轨迹与回归门禁。", small),
            p("<b>对界面</b><br/>确认界面状态与 API、工作流、权限逻辑相互对应。", small),
            p("<b>跑起来</b><br/>按部署说明本地运行，观察成功、失败与重试路径。", small),
        ],
        [
            p("<b>首页作品集</b><br/>展示定位、主项目和能力结构。", small),
            p("<b>项目证据室</b><br/>集中展示边界、评测、失败案例和复核路径。", small),
            p("<b>GitHub README</b><br/>查看实现范围、运行方式和测试目录。", small),
            p("<b>PeopleOps 演示</b><br/>90 秒视频展示问答、引用、审批和记录。", small),
        ],
    ],
    colWidths=[right_w / 4] * 4,
)
verify_path.setStyle(
    table_style(
        [
            ("BACKGROUND", (0, 0), (-1, -1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)

main = Table(
    [
        [p("01 个人优势", h2)],
        [boxed(p(summary, body), right_w, SOFT, pad=5)],
        [metrics],
        [p("02 工作经历", h2)],
        [work_table],
        [p("03 旗舰项目", h2)],
        [flagship],
        [p("04 其它项目索引", h2)],
        [project_index],
        [p("05 岗位匹配", h2)],
        [match_table],
        [p("06 背景迁移", h2)],
        [background_box],
        [p("07 作品验证路径", h2)],
        [verify_path],
    ],
    colWidths=[right_w],
)
main.setStyle(
    table_style(
        [
            ("BOTTOMPADDING", (0, 0), (0, 0), 2.4),
            ("BOTTOMPADDING", (0, 1), (0, 1), 4.2),
            ("BOTTOMPADDING", (0, 2), (0, 2), 4.2),
            ("BOTTOMPADDING", (0, 3), (0, 3), 2.4),
            ("BOTTOMPADDING", (0, 4), (0, 4), 4.2),
            ("BOTTOMPADDING", (0, 5), (0, 5), 2.4),
            ("BOTTOMPADDING", (0, 6), (0, 6), 4.2),
            ("BOTTOMPADDING", (0, 7), (0, 7), 2.4),
            ("BOTTOMPADDING", (0, 8), (0, 8), 4.2),
            ("BOTTOMPADDING", (0, 9), (0, 9), 2.4),
            ("BOTTOMPADDING", (0, 10), (0, 10), 4.2),
            ("BOTTOMPADDING", (0, 11), (0, 11), 2.4),
            ("BOTTOMPADDING", (0, 12), (0, 12), 4.2),
            ("BOTTOMPADDING", (0, 13), (0, 13), 2.4),
        ]
    )
)

layout = Table([[sidebar, main]], colWidths=[left_w, right_col_w], rowHeights=[layout_h])
layout.setStyle(
    table_style(
        [
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("LINEBEFORE", (1, 0), (1, 0), 0.45, LINE),
            ("LEFTPADDING", (0, 0), (0, 0), 5),
            ("RIGHTPADDING", (0, 0), (0, 0), 5),
            ("TOPPADDING", (0, 0), (0, 0), 5.5),
            ("BOTTOMPADDING", (0, 0), (0, 0), 5.5),
            ("LEFTPADDING", (1, 0), (1, 0), 7),
            ("RIGHTPADDING", (1, 0), (1, 0), 0),
            ("TOPPADDING", (1, 0), (1, 0), 5.5),
            ("BOTTOMPADDING", (1, 0), (1, 0), 5.5),
        ]
    )
)
story.append(layout)

doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
shutil.copyfile(FINAL_PDF, WEB_RESUME)
print(FINAL_PDF)
print(WEB_RESUME)
