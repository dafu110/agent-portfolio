import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = (ROOT / "index.html", ROOT / "cases" / "index.html")
CSS_FILES = tuple(ROOT / name for name in ("base.css", "components.css", "home.css", "responsive.css"))


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.videos = []
        self.sources = []
        self.tracks = []
        self.meta = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a":
            self.links.append(values)
        elif tag == "img":
            self.images.append(values)
        elif tag == "video":
            self.videos.append(values)
        elif tag == "source":
            self.sources.append(values)
        elif tag == "track":
            self.tracks.append(values)
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "button":
            self.buttons.append(values)


def parse(path):
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class SiteAuditTests(unittest.TestCase):
    @staticmethod
    def homepage_section(homepage, section_id):
        match = re.search(
            rf'<section id="{re.escape(section_id)}"(?:\s|>).*?</section>',
            homepage,
            re.DOTALL,
        )
        if not match:
            raise AssertionError(f"missing section #{section_id}")
        return match.group(0)

    def test_homepage_has_distinct_positioning_statement(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        visible_text = re.sub(r"<[^>]+>", "", homepage)
        self.assertEqual(len(re.findall(r'class="[^"]*\bsignature-line\b[^"]*"', homepage)), 1)
        self.assertIn("把复杂业务规则，设计成可执行、可审批、可验证的企业 AI Agent。", visible_text)
        self.assertIn("AI Agent 产品 / 应用工程", visible_text)
        self.assertIn('href="home.css"', homepage)
        self.assertTrue((ROOT / "home.css").is_file())
        self.assertIn("scroll-margin-top: 64px", (ROOT / "base.css").read_text(encoding="utf-8"))
        self.assertTrue(all(path.is_file() for path in CSS_FILES))
        for path in CSS_FILES:
            self.assertLess(len(path.read_text(encoding="utf-8").splitlines()), 1000, path)

    def test_multiline_display_headings_use_shared_alignment_system(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r'class="[^"]*\bdisplay-lines\b[^"]*"', homepage)), 0)
        self.assertEqual(len(re.findall(r'class="[^"]*\bdisplay-lines\b[^"]*"', evidence_room)), 1)
        css = (ROOT / "base.css").read_text(encoding="utf-8")
        self.assertNotIn("text-align-last: justify", css)
        hero = re.search(r'<h1[^>]*id="hero-title"[^>]*>(.*?)</h1>', homepage, re.DOTALL)
        self.assertIsNotNone(hero)
        self.assertEqual(hero.group(1), "傅孟涵")

    def test_homepage_surfaces_relevant_experience_and_prototype_boundary(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="experience"', homepage)
        self.assertIn("跨专业协调", homepage)
        self.assertIn("评审交付", homepage)
        self.assertNotIn("个人 AI 应用项目实践", homepage)
        career_heading = re.search(r'<h2 id="experience-title">(.*?)</h2>', homepage, re.DOTALL)
        self.assertIsNotNone(career_heading)
        lines = re.findall(r"<span>(.*?)</span>", career_heading.group(1))
        self.assertEqual(lines, ["复杂协同经验", "沉淀交付能力"])
        self.assertIn("建筑项目经历", homepage)

    def test_homepage_uses_verified_career_timeline_without_old_personal_fields(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        experience = self.homepage_section(homepage, "experience")
        employers = (
            "中国市政工程华北设计研究总院",
            "北京土人城市规划设计股份有限公司",
            "北京市建筑设计研究院股份有限公司",
            "北京创研建筑设计中心",
        )
        for employer in employers:
            self.assertIn(employer, experience)
        self.assertEqual(experience.count('class="career-entry"'), 4)
        self.assertIn("<dt>地点</dt><dd><strong>北京 · 可在北京工作</strong></dd>", homepage)
        self.assertIn("<dt>状态</dt><dd><strong>随时到岗</strong><span>现场 / 混合 / 远程均可</span></dd>", homepage)
        for private_or_stale in ("34 岁", "男", "15k", "20k", "建筑师、室内设计师"):
            self.assertNotIn(private_or_stale, homepage)

    def test_career_timeline_uses_verified_representative_project_scale(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        experience = self.homepage_section(homepage, "experience")
        for evidence in (
            "齐河县国家现代农业产业园综合服务中心",
            "占地 5.25 万㎡",
            "建筑面积 2.9 万㎡",
            "外径 103.8 米",
        ):
            self.assertIn(evidence, experience)
        self.assertNotIn("效率提升 60%", homepage)

    def test_career_section_includes_second_public_representative_scheme(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        experience = self.homepage_section(homepage, "experience")
        for evidence in (
            "乐清市盐盆山清和公园一体化建设工程—山顶建筑设计方案",
            "3657㎡",
            "方案设计一等奖",
            "大跨度木结构",
        ):
            self.assertIn(evidence, experience)
        self.assertNotIn("大赋建筑", experience)
        self.assertEqual(experience.count("代表方案"), 2)
        self.assertEqual(experience.count('class="career-scheme"'), 2)
        self.assertIn('class="career-schemes"', experience)
        self.assertNotIn('class="career-project"', experience)
        self.assertNotIn("xhslink.com", experience)
        self.assertNotIn("查看公开项目", experience)
        self.assertNotIn("独立设计", experience)
        self.assertNotIn("主创", experience)

    def test_desktop_section_copy_is_compact_and_unbroken(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        stylesheet = (ROOT / "home.css").read_text(encoding="utf-8")
        for text in (
            "一个旗舰案例讲清业务判断、工程实现与验证闭环，三个项目补充 Agent 工作流、RAG 与受控执行能力。",
            "从四个原型抽象出产品定义、可信知识、工作流工程和可验证交付；传统经历作为复杂协同的迁移证据。",
            "把模糊需求、多方协同与复杂约束，转为边界清晰、可测试、可追溯的企业 AI 工作流。",
        ):
            self.assertIn(text, homepage)
        self.assertIn(".flagship-shot .shot-caption strong", stylesheet)
        self.assertNotIn("white-space: nowrap", stylesheet)
        self.assertIn("min-width: 1200px", stylesheet)
        self.assertNotIn("min-width: 1120px", stylesheet)
        self.assertIn("求职方向", homepage)
        self.assertIn("<h3>PeopleOps 智能工作台</h3>", homepage)
        self.assertNotIn("查看中文简历", homepage)

    def test_public_html_does_not_expose_phone_number(self):
        for path in HTML_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"158\s*1120\s*3776", path)
            self.assertNotIn('"telephone"', text, path)

    def test_homepage_contact_cta_uses_inline_dialog(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        background_actions = re.search(
            r'<div class="background-actions">(.*?)</div>',
            homepage,
            re.DOTALL,
        )
        self.assertIsNotNone(background_actions)
        self.assertIn("data-contact-open", background_actions.group(1))
        self.assertNotIn("mailto:", background_actions.group(1))
        self.assertIn("data-contact-dialog", homepage)
        self.assertIn("data-copy-email", homepage)

    def test_resume_ctas_lead_to_the_two_explicit_versions(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(homepage.count('href="#resume-versions"'), 2)
        self.assertIn('id="resume-versions"', homepage)
        self.assertEqual(homepage.count('href="assets/resume.pdf"'), 1)
        self.assertEqual(homepage.count('href="assets/resume-agent-engineer.pdf"'), 2)

    def test_local_links_and_fragments_exist(self):
        for path in HTML_FILES:
            parser = parse(path)
            for link in parser.links:
                href = link.get("href", "")
                if not href or href.startswith(("http", "mailto:", "tel:")):
                    continue
                relative, _, fragment = href.partition("#")
                target = (path.parent / relative).resolve() if relative else path
                self.assertTrue(target.exists(), f"{path}: missing {href}")
                if fragment and target.suffix == ".html":
                    self.assertIn(fragment, parse(target).ids, f"{path}: missing #{fragment}")

    def test_image_dimensions_match_files(self):
        for path in HTML_FILES:
            for image in parse(path).images:
                source = (path.parent / image["src"]).resolve()
                with Image.open(source) as asset:
                    self.assertEqual(int(image["width"]), asset.width, source)
                    self.assertEqual(int(image["height"]), asset.height, source)

    def test_only_first_content_image_is_eager(self):
        for path in HTML_FILES:
            images = parse(path).images
            eager = [image for image in images if image.get("loading") == "eager"]
            self.assertLessEqual(len(eager), 1, path)
            for image in images[1:]:
                self.assertEqual(image.get("decoding"), "async", f"{path}: {image['src']}")

    def test_mobile_navigation_control_exists(self):
        for path in HTML_FILES:
            parser = parse(path)
            controls = [button for button in parser.buttons if button.get("aria-controls") == "site-nav"]
            self.assertEqual(len(controls), 1, path)

    def test_evidence_room_has_quick_project_index(self):
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(evidence_room.count('class="evidence-index"'), 1)
        for fragment in ("#peopleops", "#researchops", "#knowflow", "#data-analyst"):
            self.assertIn(f'href="{fragment}"', evidence_room)
        self.assertEqual(evidence_room.count('class="case-title-parts"'), 4)

    def test_share_metadata_is_deployment_configurable(self):
        for path in HTML_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertIn('rel="canonical"', text, path)
            self.assertIn('property="og:url"', text, path)
            self.assertIn('property="og:image:width"', text, path)
            self.assertIn('property="og:image:height"', text, path)
            meta = parse(path).meta
            image_meta = next(item for item in meta if item.get("property") == "og:image")
            width_meta = next(item for item in meta if item.get("property") == "og:image:width")
            height_meta = next(item for item in meta if item.get("property") == "og:image:height")
            self.assertTrue(image_meta["content"].endswith("/assets/portfolio-social-preview.png"))
            self.assertEqual(width_meta["content"], "1200")
            self.assertEqual(height_meta["content"], "630")
        with Image.open(ROOT / "assets" / "portfolio-social-preview.png") as preview:
            self.assertEqual(preview.size, (1200, 630))

    def test_new_tab_links_are_hardened(self):
        for path in HTML_FILES:
            for link in parse(path).links:
                if link.get("target") == "_blank":
                    rel = set(link.get("rel", "").split())
                    self.assertTrue("noreferrer" in rel or "noopener" in rel, f"{path}: {link}")

    def test_no_forced_break_all(self):
        css = "\n".join(path.read_text(encoding="utf-8") for path in CSS_FILES)
        self.assertIsNone(re.search(r"word-break\s*:\s*break-all", css))

    def test_homepage_copy_and_mobile_demo_entry_are_recruiter_friendly(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        components = (ROOT / "components.css").read_text(encoding="utf-8")
        responsive = (ROOT / "responsive.css").read_text(encoding="utf-8")

        self.assertIn("\u7ed3\u679c\u53ef\u590d\u6838", homepage)
        self.assertIn("查看项目与代码", homepage)
        self.assertNotIn("fixture", homepage)
        self.assertNotIn("\u9ec4\u91d1\u8f68\u8ff9", homepage)
        self.assertIn('class="background-actions"', homepage)
        self.assertNotRegex(
            responsive,
            r"\.flagship-actions a:first-child\s*\{[^}]*display\s*:\s*none",
        )
        self.assertIn('content: " \u2192";', components)
        self.assertIn('content: " \u2212";', components)

    def test_long_headings_use_controlled_responsive_wrapping(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        home_css = (ROOT / "home.css").read_text(encoding="utf-8")
        responsive = (ROOT / "responsive.css").read_text(encoding="utf-8")
        hero_focus = re.search(r'<p class="hero-focus">(.*?)</p>', homepage, re.DOTALL)
        self.assertIsNotNone(hero_focus)
        self.assertEqual(hero_focus.group(1).count("<span>"), 2)
        self.assertIn(".hero-focus span", home_css)
        self.assertRegex(responsive, r"\.cta-card h2\s*\{[^}]*white-space:\s*normal")
        self.assertNotRegex(responsive, r"\.cta-card h2\s*\{[^}]*white-space:\s*nowrap")

    def test_peopleops_demo_video_is_embedded_accessibly(self):
        for path in HTML_FILES:
            parser = parse(path)
            demos = [video for video in parser.videos if video.get("data-project") == "peopleops"]
            self.assertEqual(len(demos), 1, path)
            video = demos[0]
            self.assertNotIn("controls", video, path)
            self.assertEqual(video.get("preload"), "metadata", path)
            self.assertTrue(video.get("poster"), path)
            controls = [button for button in parser.buttons if "demo-video-toggle" in button.get("class", "")]
            self.assertEqual(len(controls), 1, path)
            self.assertIn("aria-label", controls[0], path)
            sources = {source.get("type"): source for source in parser.sources}
            self.assertIn("video/mp4", sources, path)
            self.assertIn("video/webm", sources, path)
            for source in sources.values():
                asset = (path.parent / source["src"]).resolve()
                self.assertTrue(asset.is_file(), f"{path}: missing {asset}")
            captions = [track for track in parser.tracks if track.get("kind") == "captions"]
            self.assertEqual(len(captions), 1, path)
            caption_asset = (path.parent / captions[0]["src"]).resolve()
            self.assertTrue(caption_asset.is_file(), f"{path}: missing {caption_asset}")
        mp4 = ROOT / "assets" / "peopleops-real-agent-90s-1080p.mp4"
        payload = mp4.read_bytes()
        self.assertGreater(payload.find(b"moov"), 0)
        self.assertGreater(payload.find(b"mdat"), 0)
        self.assertLess(payload.find(b"moov"), payload.find(b"mdat"), "MP4 should be fast-start optimized")
        captions = (ROOT / "assets" / "peopleops-demo-zh.vtt").read_text(encoding="utf-8")
        self.assertTrue(captions.startswith("WEBVTT"))
        self.assertEqual(captions.count(" --> "), 6)

    def test_project_periods_and_product_judgments_are_visible(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(homepage.count('class="project-period"'), 4)
        self.assertEqual(homepage.count("<dt>个人贡献</dt>"), 1)
        self.assertEqual(homepage.count("<dt>关键决策</dt>"), 3)
        self.assertEqual(evidence_room.count('class="project-period"'), 4)
        self.assertEqual(evidence_room.count('<span>个人贡献</span>'), 4)

    def test_homepage_puts_ai_evidence_before_architecture_experience(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertLess(homepage.index('id="work"'), homepage.index('id="capability"'))
        self.assertLess(homepage.index('id="capability"'), homepage.index('id="experience"'))
        self.assertLess(homepage.index('href="#work"'), homepage.index('href="#capability"'))
        self.assertLess(homepage.index('href="#capability"'), homepage.index('href="#experience"'))
        self.assertIn("独立完成 4 个 Agent 工作流原型", homepage)

    def test_peopleops_homepage_proof_is_compact_without_metric_repetition(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        flagship = re.search(
            r'<article id="project-peopleops".*?</article>', homepage, re.DOTALL
        ).group(0)
        self.assertIn('class="flagship-evidence"', flagship)
        self.assertEqual(homepage.count("47 / 47"), 2)
        self.assertEqual(homepage.count("25 / 25"), 2)
        for label in ("业务问题", "个人贡献", "关键实现"):
            self.assertIn(f"<dt>{label}</dt>", flagship)
        self.assertNotIn("<dt>验证结果</dt>", flagship)

    def test_homepage_projects_are_scan_focused(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        fact_groups = re.findall(r'<dl class="resume-facts">(.*?)</dl>', homepage, re.DOTALL)
        self.assertEqual(len(fact_groups), 1)
        compact_groups = re.findall(r'<dl class="compact-facts">(.*?)</dl>', homepage, re.DOTALL)
        self.assertEqual(len(compact_groups), 3)
        for compact in compact_groups:
            self.assertEqual(compact.count("<div>"), 2)
        for facts in fact_groups:
            self.assertEqual(facts.count("<div>"), 3)
            self.assertIn("业务问题", facts)
            self.assertIn("个人贡献", facts)
            self.assertIn("关键实现", facts)
        self.assertNotIn("<dt>技术/系统边界</dt>", homepage)
        self.assertNotIn("<dt>GitHub README</dt>", homepage)
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(evidence_room.count("<span>用户场景</span>"), 4)
        self.assertEqual(evidence_room.count("<span>项目边界</span>"), 4)

    def test_homepage_uses_one_flagship_showcase_without_duplicate_index(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        stylesheet = (ROOT / "home.css").read_text(encoding="utf-8")
        for project_id in ("project-peopleops", "project-researchops", "project-knowflow", "project-data"):
            self.assertIn(f'id="{project_id}"', homepage)
        self.assertEqual(homepage.count('class="shot-caption"'), 1)
        self.assertEqual(homepage.count('class="supporting-project"'), 3)
        self.assertNotIn('class="summary-band"', homepage)
        self.assertNotIn('class="project-jump', homepage)
        self.assertNotIn('class="surface-pin', homepage)
        self.assertEqual(evidence_room.count('class="case-visual"'), 4)
        self.assertIn('href="#peopleops-demo"', homepage)
        self.assertIn('id="peopleops-demo"', homepage)
        self.assertIn("scroll-margin-top: 80px", stylesheet)
        self.assertNotIn("公开版本集中开发", homepage)

    def test_project_periods_use_machine_readable_dates(self):
        expected_counts = {ROOT / "index.html": 8, ROOT / "cases" / "index.html": 8}
        for path, expected_count in expected_counts.items():
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r'datetime="\d{4}-\d{2}-\d{2}/')
            self.assertEqual(len(re.findall(r'<time datetime="\d{4}-\d{2}-\d{2}">', text)), expected_count, path)

    def test_peopleops_summary_matches_published_evaluation(self):
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        self.assertIn("47 / 47", evidence_room)
        self.assertIn("25 / 25", evidence_room)
        self.assertNotIn("<strong>47 / 25</strong>", evidence_room)
        self.assertNotIn("<strong>40 项</strong>", evidence_room)

    def test_peopleops_eval_record_has_required_provenance(self):
        record = ROOT / "evidence" / "peopleops-eval-2026-07-13.json"
        self.assertTrue(record.is_file(), record)
        text = record.read_text(encoding="utf-8")
        for expected in (
            '"run_date": "2026-07-13"',
            '"configured_chat_model": "deepseek-chat"',
            '"configured_embedding_model": "BAAI/bge-small-zh-v1.5"',
            '"offline_cases": 25',
            '"unit_tests": 47',
            '"failure_case": {',
            '"fix_commit": "dfa4bd6"',
        ):
            self.assertIn(expected, text)
        cases = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="peopleops-eval"', cases)
        self.assertIn("2026-07-13", cases)

    def test_portfolio_is_recruiter_scannable_and_pages_ready(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        evidence_room = (ROOT / "cases" / "index.html").read_text(encoding="utf-8")
        workflow = ROOT / ".github" / "workflows" / "pages.yml"

        self.assertIn("北京 · 可在北京工作", homepage)
        self.assertIn("随时到岗", homepage)
        self.assertIn("现场 / 混合 / 远程均可", homepage)
        self.assertIn("HRBP 与招聘运营", homepage)
        for label in ("用户场景", "关键判断", "当前证据", "项目边界"):
            self.assertEqual(evidence_room.count(f"<span>{label}</span>"), 4)
        for case in re.findall(r'<article id="(?:peopleops|researchops|knowflow|data-analyst)".*?</article>', evidence_room, re.DOTALL):
            self.assertLess(case.index('class="case-file-grid"'), case.index('class="case-visual"'))
        self.assertTrue((ROOT / ".nojekyll").is_file())
        self.assertTrue(workflow.is_file())
        workflow_text = workflow.read_text(encoding="utf-8")
        self.assertIn("actions/upload-pages-artifact", workflow_text)
        self.assertIn("actions/deploy-pages", workflow_text)
        responsive = (ROOT / "responsive.css").read_text(encoding="utf-8")
        self.assertIn(".case-file-grid section {\n    min-height: auto;", responsive)


if __name__ == "__main__":
    unittest.main()
