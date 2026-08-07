import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = (ROOT / "index.html", ROOT / "cases" / "index.html")
PUBLIC_TEXT_FILES = HTML_FILES + (ROOT / "site.js", ROOT / "make_chinese_resume_pdf.py")
OLD_PROJECTS = ("ResearchOps", "KnowFlow", "Data Analyst", "researchops", "knowflow", "data-analyst")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.videos = []
        self.sources = []
        self.tracks = []
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
        elif tag == "button":
            self.buttons.append(values)


def read(path):
    return path.read_text(encoding="utf-8")


def parse(path):
    parser = DocumentParser()
    parser.feed(read(path))
    return parser


class SiteAuditTests(unittest.TestCase):
    def test_public_site_and_generator_are_english_only(self):
        for path in PUBLIC_TEXT_FILES:
            self.assertIsNone(CJK_RE.search(read(path)), path)

    def test_homepage_is_current_ai_practice_resume(self):
        homepage = read(ROOT / "index.html")
        for phrase in (
            "AI Practice Consultant",
            "practical, people-facing AI adoption",
            "Opportunity Discovery",
            "Workflow Prototyping",
            "Colleague Enablement",
            "Guidance & Scaling",
            "10 years leading complex project delivery",
        ):
            self.assertIn(phrase, homepage)
        self.assertNotIn("AI Practice Consultant /", homepage)
        self.assertNotIn("resume-agent-engineer.pdf", homepage)
        self.assertEqual(homepage.count('href="assets/resume.pdf"'), 2)
        self.assertEqual(homepage.count('class="supporting-project"'), 2)
        order = [
            homepage.index('id="project-ai-practice"'),
            homepage.index('id="project-buildloop"'),
            homepage.index('id="project-peopleops"'),
        ]
        self.assertEqual(order, sorted(order))

    def test_homepage_projects_are_all_video_first(self):
        homepage = read(ROOT / "index.html")
        parser = parse(ROOT / "index.html")
        projects = {video.get("data-project") for video in parser.videos}
        self.assertEqual(projects, {"ai-practice", "buildloop-home", "peopleops-home"})
        self.assertIn('poster="assets/ai-practice-demo-first-frame.png"', homepage)
        self.assertIn('poster="assets/peopleops-intelligence-console.png"', homepage)
        self.assertIn('src="assets/buildloop-ai-complete-flow.webm"', homepage)
        toggles = [button for button in parser.buttons if "demo-video-toggle" in button.get("class", "")]
        self.assertEqual(len(toggles), 3)

    def test_cases_page_matches_three_project_evidence_room(self):
        cases = read(ROOT / "cases" / "index.html")
        self.assertEqual(cases.count('class="case-file"'), 3)
        self.assertEqual(cases.count('class="case-title-parts"'), 3)
        for fragment in ("#ai-practice", "#buildloop", "#peopleops"):
            self.assertIn(f'href="{fragment}"', cases)
        for label in ("User scenario", "Key decision", "Current evidence", "Project boundary"):
            self.assertIn(label, cases)
        self.assertIn('data-project="ai-practice-case"', cases)
        self.assertIn('data-project="buildloop-case"', cases)
        self.assertIn('data-project="peopleops"', cases)
        self.assertIn('poster="../assets/peopleops-intelligence-console.png"', cases)

    def test_no_old_project_names_in_public_html(self):
        for path in HTML_FILES:
            text = read(path)
            for old in OLD_PROJECTS:
                self.assertNotIn(old, text, path)

    def test_local_links_fragments_and_media_exist(self):
        for path in HTML_FILES:
            parser = parse(path)
            refs = []
            refs.extend(("href", link.get("href", "")) for link in parser.links)
            refs.extend(("src", image.get("src", "")) for image in parser.images)
            refs.extend(("poster", video.get("poster", "")) for video in parser.videos)
            refs.extend(("source", source.get("src", "")) for source in parser.sources)
            refs.extend(("track", track.get("src", "")) for track in parser.tracks)
            for attr, value in refs:
                if not value or value.startswith(("http", "mailto:", "tel:")):
                    continue
                if value.startswith("#"):
                    self.assertIn(value[1:], parser.ids, f"{path}: missing local anchor {value}")
                    continue
                relative, _, fragment = value.partition("#")
                target = (path.parent / unquote(relative)).resolve()
                self.assertTrue(target.exists(), f"{path}: missing {attr} {value}")
                if fragment and target.suffix == ".html":
                    self.assertIn(fragment, parse(target).ids, f"{path}: missing #{fragment}")

    def test_declared_image_dimensions_match_files(self):
        for path in HTML_FILES:
            for image in parse(path).images:
                source = (path.parent / unquote(image["src"])).resolve()
                with Image.open(source) as asset:
                    self.assertEqual(int(image["width"]), asset.width, source)
                    self.assertEqual(int(image["height"]), asset.height, source)


if __name__ == "__main__":
    unittest.main()
