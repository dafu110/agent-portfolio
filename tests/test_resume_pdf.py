import re
import subprocess
import sys
import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "make_chinese_resume_pdf.py"
PRODUCT_OUT = ROOT / "output" / "pdf" / "fu-menghan-ai-agent-resume-one-page.pdf"
PRODUCT_WEB = ROOT / "assets" / "resume.pdf"
ENGINEER_OUT = ROOT / "output" / "pdf" / "fu-menghan-ai-agent-engineer-resume-one-page.pdf"
ENGINEER_WEB = ROOT / "assets" / "resume-agent-engineer.pdf"
OLD_PROJECTS = ("ResearchOps", "KnowFlow", "Data Analyst", "researchops", "knowflow", "data-analyst")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def pdf_text(path):
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


class ResumePdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(GENERATOR)], cwd=ROOT, check=True)
        cls.product_reader = PdfReader(str(PRODUCT_OUT))
        cls.product_text = pdf_text(PRODUCT_OUT)
        cls.product_compact = "".join(cls.product_text.split())

    def test_single_ai_practice_pdf_is_one_page_and_synced_to_web_asset(self):
        self.assertEqual(len(self.product_reader.pages), 1)
        self.assertEqual(PRODUCT_OUT.read_bytes(), PRODUCT_WEB.read_bytes())
        self.assertFalse(ENGINEER_WEB.exists())
        self.assertFalse(ENGINEER_OUT.exists())

    def test_pdf_is_english_and_targets_ai_practice_consultant(self):
        self.assertIsNone(CJK_RE.search(self.product_text))
        for phrase in (
            "AIPracticeConsultant",
            "people-facingAIadoption",
            "OpportunityDiscovery",
            "WorkflowPrototyping",
            "Enablement&Scaling",
        ):
            self.assertIn(phrase, self.product_compact)
        self.assertNotIn("AIPracticeConsultant/", self.product_compact)

    def test_pdf_uses_current_three_project_story(self):
        for current in ("ArchMind", "ArchitectureAIPracticeWorkspace", "BuildLoopAI", "PeopleOps"):
            self.assertIn(current, self.product_compact)
        for metric in ("4", "283", "47/47", "25/25"):
            self.assertIn(metric, self.product_compact)

    def test_old_project_and_engineer_variant_names_are_removed(self):
        generator_text = GENERATOR.read_text(encoding="utf-8")
        self.assertIsNone(CJK_RE.search(generator_text))
        for old in OLD_PROJECTS:
            self.assertNotIn(old, self.product_text)
            self.assertNotIn(old, generator_text)
        for stale in ("resume-agent-engineer", "AI Practice Consultant /", "--variant", "IS_ENGINEER"):
            self.assertNotIn(stale, generator_text)

    def test_public_links_are_embedded(self):
        annotations = self.product_reader.pages[0].get("/Annots") or []
        uris = []
        for annotation in annotations:
            action = annotation.get_object().get("/A")
            if action and action.get("/URI"):
                uris.append(str(action["/URI"]))
        for expected in (
            "mailto:poeticarch@163.com",
            "https://github.com/dafu110",
            "https://dafu110.github.io/agent-portfolio/",
            "https://github.com/dafu110/Architecture-AI-Practice-Workspace",
            "https://github.com/dafu110/BuildLoop-Al",
            "https://github.com/dafu110/peopleops-intelligence-agent",
        ):
            self.assertIn(expected, uris)


if __name__ == "__main__":
    unittest.main()
