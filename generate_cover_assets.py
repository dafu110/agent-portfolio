from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


OUT = Path(__file__).parent / "assets"
W, H = 1600, 1000

COLORS = {
    "bg": "#f6f4ef",
    "surface": "#ffffff",
    "surface_2": "#edf2ef",
    "text": "#17211d",
    "muted": "#5f6962",
    "line": "#d9ded7",
    "green": "#145c4a",
    "green_dark": "#0c3d33",
    "gold": "#9a6b21",
    "blue": "#315a7d",
    "red": "#a94f42",
}


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


F = {
    "eyebrow": font(30, True),
    "title": font(66, True),
    "subtitle": font(34, True),
    "body": font(28, False),
    "small": font(22, False),
    "tiny": font(18, False),
}


def rr(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, fill=None, fnt=None, anchor=None):
    draw.text(xy, value, fill=fill or COLORS["text"], font=fnt or F["body"], anchor=anchor)


def line(draw, points, fill=None, width=4):
    draw.line(points, fill=fill or COLORS["green"], width=width, joint="curve")


def arrow(draw, start, end, fill=None):
    fill = fill or COLORS["green"]
    line(draw, [start, end], fill, 5)
    x1, y1 = start
    x2, y2 = end
    if x2 >= x1:
        tri = [(x2, y2), (x2 - 18, y2 - 10), (x2 - 18, y2 + 10)]
    else:
        tri = [(x2, y2), (x2 + 18, y2 - 10), (x2 + 18, y2 + 10)]
    draw.polygon(tri, fill=fill)


def base():
    img = Image.new("RGB", (W, H), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    rr(draw, (48, 48, W - 48, H - 48), 26, COLORS["surface"], COLORS["line"], 2)
    return img, draw


def badge(draw, xy, label, color=None):
    x, y = xy
    bbox = draw.textbbox((0, 0), label, font=F["small"])
    width = bbox[2] - bbox[0] + 42
    rr(draw, (x, y, x + width, y + 48), 24, COLORS["surface_2"], COLORS["line"], 1)
    text(draw, (x + 21, y + 11), label, color or COLORS["green_dark"], F["small"])
    return x + width


def top_title(draw, eyebrow, title_value, subtitle):
    text(draw, (110, 105), eyebrow, COLORS["gold"], F["eyebrow"])
    text(draw, (110, 160), title_value, COLORS["text"], F["title"])
    text(draw, (112, 252), subtitle, COLORS["muted"], F["body"])


def metric_card(draw, x, y, big, label, color=None):
    rr(draw, (x, y, x + 260, y + 150), 18, COLORS["surface"], COLORS["line"], 2)
    text(draw, (x + 26, y + 28), big, color or COLORS["green"], F["subtitle"])
    text(draw, (x + 28, y + 88), label, COLORS["muted"], F["small"])


def node(draw, x, y, title_value, label, color=None, w=250):
    rr(draw, (x, y, x + w, y + 118), 16, COLORS["surface"], COLORS["line"], 2)
    text(draw, (x + 24, y + 22), title_value, color or COLORS["green_dark"], F["body"])
    text(draw, (x + 24, y + 68), label, COLORS["muted"], F["small"])


def make_hero():
    img, draw = base()
    rr(draw, (110, 100, 1490, 240), 22, COLORS["green_dark"])
    text(draw, (150, 142), "AI Agent Capability Map", "#ffffff", F["subtitle"])
    text(draw, (150, 194), "Plan · Retrieve · Act · Approve · Evaluate", "#cfe4dc", F["small"])
    badge(draw, (1110, 146), "Portfolio-ready")
    badge(draw, (1330, 146), "4 projects")

    center = (800, 555)
    rr(draw, (595, 405, 1005, 705), 28, COLORS["green_dark"])
    text(draw, (800, 488), "AI Agent", "#ffffff", F["title"], "mm")
    text(draw, (800, 574), "Productized Workflow", "#cfe4dc", F["body"], "mm")
    text(draw, (800, 640), "业务场景 · 工具编排 · 质量验证", "#cfe4dc", F["small"], "mm")

    modules = [
        (160, 330, "RAG", "知识库 / 引用", COLORS["blue"]),
        (1180, 330, "Tools", "MCP / SQL / Python", COLORS["green"]),
        (160, 690, "Approval", "Human-in-the-loop", COLORS["red"]),
        (1180, 690, "Eval", "Golden traces", COLORS["gold"]),
    ]
    for x, y, title_value, label, color in modules:
        node(draw, x, y, title_value, label, color, 260)
        start = (x + 260, y + 58) if x < center[0] else (x, y + 58)
        end = (595, center[1]) if x < center[0] else (1005, center[1])
        arrow(draw, start, end, color)

    rr(draw, (330, 815, 1270, 900), 18, COLORS["surface_2"], COLORS["line"], 2)
    text(draw, (372, 842), "Built for solution roles:", COLORS["green_dark"], F["small"])
    text(draw, (615, 842), "AI Agent PM · AI Solution Expert · RAG Product", COLORS["muted"], F["small"])
    img.save(OUT / "hero-agent-overview.png", quality=95)


def make_peopleops():
    img, draw = base()
    top_title(draw, "PEOPLEOPS INTELLIGENCE", "HR Agent Console", "政策问答、简历匹配、候选人跟进、审批流与审计留痕")
    steps = [
        ("Intake", "简历 / JD / 上下文", COLORS["blue"]),
        ("Route", "政策 / 匹配 / 行动", COLORS["green"]),
        ("Evidence", "RAG 引用证据", COLORS["gold"]),
        ("Approval", "候选人行动审批", COLORS["red"]),
        ("Audit", "哈希链审计日志", COLORS["green_dark"]),
    ]
    y = 470
    prev = None
    for idx, (t, l, c) in enumerate(steps):
        x = 110 + idx * 292
        node(draw, x, y, t, l, c, 230)
        if prev:
            arrow(draw, (prev + 230, y + 60), (x, y + 60), COLORS["line"])
        prev = x
    rr(draw, (110, 710, 620, 860), 18, COLORS["surface_2"], COLORS["line"], 2)
    text(draw, (150, 750), "Fit Analysis", COLORS["green_dark"], F["subtitle"])
    text(draw, (150, 812), "Resume ↔ JD 匹配度、优势、风险与追问建议", COLORS["muted"], F["small"])
    rr(draw, (700, 710, 1490, 860), 18, COLORS["green_dark"])
    text(draw, (740, 750), "Enterprise Controls", "#ffffff", F["subtitle"])
    text(draw, (740, 812), "RBAC · Tenant Scope · PII Redaction · Approval Gate", "#cfe4dc", F["small"])
    img.save(OUT / "peopleops-cover.png", quality=95)


def make_researchops():
    img, draw = base()
    top_title(draw, "RESEARCHOPS AGENT", "Research Workflow Console", "文档摄取、RAG 引用回答、工具调用、追踪时间线与评测门禁")
    node(draw, 140, 450, "Planner", "stage / risk / confidence", COLORS["blue"], 300)
    node(draw, 650, 330, "Tool Agent", "SQL / Python / Report / MCP", COLORS["green"], 320)
    node(draw, 650, 590, "RAG Research", "grounded citations", COLORS["gold"], 320)
    node(draw, 1160, 450, "Approval", "risky actions wait", COLORS["red"], 300)
    arrow(draw, (440, 508), (650, 390), COLORS["blue"])
    arrow(draw, (440, 508), (650, 650), COLORS["gold"])
    arrow(draw, (970, 390), (1160, 508), COLORS["green"])
    arrow(draw, (970, 650), (1160, 508), COLORS["gold"])
    rr(draw, (160, 760, 1440, 870), 18, COLORS["surface_2"], COLORS["line"], 2)
    for i, label in enumerate(["created", "planner", "tool_call", "rag_answer", "approval", "completed"]):
        x = 210 + i * 220
        draw.ellipse((x, 795, x + 24, 819), fill=COLORS["green"])
        text(draw, (x + 36, 790), label, COLORS["muted"], F["small"])
        if i < 5:
            line(draw, [(x + 24, 807), (x + 190, 807)], COLORS["line"], 4)
    img.save(OUT / "researchops-cover.png", quality=95)


def make_knowflow():
    img, draw = base()
    top_title(draw, "KNOWFLOW RAG", "Trustworthy Knowledge Agent", "企业知识库、权限过滤、混合检索、重排、引用与幻觉检测")
    steps = [
        ("Documents", "PDF / Markdown / Text", COLORS["blue"]),
        ("Chunking", "structure-aware split", COLORS["green"]),
        ("ACL Filter", "pre-ranking permission", COLORS["red"]),
        ("Hybrid Retrieve", "BM25 + vector + rerank", COLORS["gold"]),
        ("Answer", "citations + faithfulness", COLORS["green_dark"]),
    ]
    for idx, (t, l, c) in enumerate(steps):
        x = 120 + idx * 292
        node(draw, x, 450, t, l, c, 230)
        if idx:
            arrow(draw, (x - 62, 508), (x, 508), COLORS["line"])
    rr(draw, (150, 710, 690, 860), 18, COLORS["surface_2"], COLORS["line"], 2)
    text(draw, (190, 752), "Quality Gate", COLORS["green_dark"], F["subtitle"])
    text(draw, (190, 812), "recall@k · citation accuracy · leakage=0", COLORS["muted"], F["small"])
    rr(draw, (780, 710, 1450, 860), 18, COLORS["surface"])
    for i, width in enumerate([520, 420, 470]):
        y = 750 + i * 36
        rr(draw, (820, y, 820 + width, y + 16), 8, COLORS["accent_soft"] if "accent_soft" in COLORS else "#dce9e4")
    text(draw, (820, 818), "Evidence-first answer with source locators", COLORS["muted"], F["small"])
    img.save(OUT / "knowflow-cover.png", quality=95)


def make_data():
    img, draw = base()
    top_title(draw, "DATA ANALYST AGENT", "Analysis SaaS Prototype", "CSV / Excel 摄取、数据画像、SQL / Python 分析、图表建议与报告导出")
    node(draw, 150, 420, "Upload", "CSV / Excel / DB", COLORS["blue"], 260)
    node(draw, 500, 420, "Profile", "fields / quality / types", COLORS["green"], 280)
    node(draw, 880, 420, "Analyze", "SQL + Python plan", COLORS["gold"], 280)
    node(draw, 1240, 420, "Report", "PDF / PPTX / HTML", COLORS["red"], 260)
    arrow(draw, (410, 478), (500, 478), COLORS["line"])
    arrow(draw, (780, 478), (880, 478), COLORS["line"])
    arrow(draw, (1160, 478), (1240, 478), COLORS["line"])
    rr(draw, (160, 680, 690, 860), 18, COLORS["surface_2"], COLORS["line"], 2)
    text(draw, (200, 720), "Guarded Execution", COLORS["green_dark"], F["subtitle"])
    text(draw, (200, 782), "AST guard · read-only mode · Docker sandbox", COLORS["muted"], F["small"])
    rr(draw, (800, 660, 1440, 860), 18, COLORS["surface"], COLORS["line"], 2)
    bars = [120, 260, 180, 340, 230]
    for i, h in enumerate(bars):
        x = 870 + i * 90
        rr(draw, (x, 820 - h // 2, x + 44, 820), 8, COLORS["green"] if i != 3 else COLORS["gold"])
    line(draw, [(860, 820), (1360, 820)], COLORS["line"], 3)
    text(draw, (870, 700), "Chart suggestions + executive insight", COLORS["muted"], F["small"])
    img.save(OUT / "data-analyst-cover.png", quality=95)


def make_social_preview():
    width, height = 1200, 630
    img = Image.new("RGB", (width, height), "#f4f4f1")
    draw = ImageDraw.Draw(img)
    ink = "#171717"
    text_color = "#4b4b48"
    muted = "#777773"
    line_color = "#d7d7d2"
    accent = "#4f46e5"

    brand_font = font(18, True)
    meta_font = font(13, False)
    name_font = font(66, True)
    role_font = font(24, True)
    headline_font = font(38, True)
    body_font = font(18, False)
    proof_font = font(20, True)
    proof_label_font = font(13, False)

    text(draw, (42, 23), "傅孟涵", ink, brand_font)
    text(draw, (112, 28), "AI Agent Resume Portfolio", muted, meta_font)
    text(draw, (1150, 28), "PRODUCT + ENGINEERING", muted, meta_font, "ra")
    line(draw, [(0, 64), (1200, 64)], line_color, 1)

    text(draw, (52, 112), "AI PRODUCT / AGENT ENGINEERING / ENTERPRISE RAG", muted, meta_font)
    text(draw, (48, 142), "傅孟涵", ink, name_font)
    text(draw, (52, 224), "AI Agent 产品 / 应用工程", ink, role_font)
    text(draw, (52, 294), "把复杂业务规则，设计成可执行、", ink, headline_font)
    text(draw, (52, 344), "可审批、可验证的企业 AI Agent。", ink, headline_font)
    text(draw, (52, 420), "独立完成 4 个 Agent 工作流原型，覆盖 RAG、工具调用、", text_color, body_font)
    text(draw, (52, 450), "人工审批、评测与审计，并形成可复核的代码与测试证据。", text_color, body_font)

    proof_items = [
        ("10 年", "复杂项目交付"),
        ("4 个", "独立 Agent 原型"),
        ("47 / 47", "测试 · 25 / 25 离线案例"),
    ]
    proof_x = [52, 236, 414]
    proof_w = [150, 150, 290]
    for idx, (value, label) in enumerate(proof_items):
        x = proof_x[idx]
        if idx:
            line(draw, [(x - 18, 520), (x - 18, 592)], line_color, 1)
        text(draw, (x, 526), value, ink, proof_font)
        text(draw, (x, 562), label, muted, proof_label_font)

    card = (816, 104, 1148, 548)
    rr(draw, card, 8, "#ffffff", line_color, 1)
    portrait_path = OUT / "profile-portrait.png"
    portrait = Image.open(portrait_path).convert("RGB")
    portrait = ImageOps.fit(portrait, (132, 165), method=Image.Resampling.LANCZOS, centering=(0.5, 0.16))
    img.paste(portrait, (840, 128))
    text(draw, (998, 144), "个人项目", accent, meta_font)
    text(draw, (998, 177), "需求拆解", ink, role_font)
    text(draw, (998, 211), "原型开发", ink, role_font)
    text(draw, (998, 245), "测试评测", ink, role_font)
    line(draw, [(840, 318), (1124, 318)], line_color, 1)
    text(draw, (840, 344), "旗舰案例", muted, meta_font)
    text(draw, (840, 374), "PeopleOps 智能工作台", ink, role_font)
    text(draw, (840, 416), "RAG · Tool Calling · Approval", text_color, meta_font)
    text(draw, (840, 444), "权限 · 审计 · 离线评测", text_color, meta_font)
    text(draw, (840, 500), "90 秒真实演示", accent, proof_font)

    img.save(OUT / "portfolio-social-preview.png", quality=95)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    make_hero()
    make_peopleops()
    make_researchops()
    make_knowflow()
    make_data()
    make_social_preview()


if __name__ == "__main__":
    main()
