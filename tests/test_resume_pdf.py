import re
import subprocess
import unittest
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(
    r"C:\Users\lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)
GENERATOR = ROOT / "make_chinese_resume_pdf.py"
FINAL_PDF = ROOT / "output" / "pdf" / "fu-menghan-ai-agent-resume-one-page.pdf"
WEB_PDF = ROOT / "assets" / "resume.pdf"


class ResumePdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([str(PYTHON), str(GENERATOR)], cwd=ROOT, check=True)
        cls.reader = PdfReader(str(FINAL_PDF))
        cls.text = "\n".join(page.extract_text() or "" for page in cls.reader.pages)

    def test_resume_is_one_page_and_synced_with_website(self):
        self.assertEqual(len(self.reader.pages), 1)
        self.assertEqual(FINAL_PDF.read_bytes(), WEB_PDF.read_bytes())

    def test_resume_uses_recruiter_reading_order(self):
        headings = ["个人简介", "工作经历", "AI 项目经历", "专业能力", "教育背景"]
        positions = [self.text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        for removed in ("岗位匹配", "背景迁移", "作品验证路径"):
            self.assertNotIn(removed, self.text)

    def test_personal_ai_projects_are_not_listed_as_employment(self):
        work = self.text.split("工作经历", 1)[1].split("AI 项目经历", 1)[0]
        self.assertNotIn("个人 AI 应用项目实践", work)
        self.assertIn("建筑设计 / 项目负责人", work)

    def test_body_copy_is_legible(self):
        source = GENERATOR.read_text(encoding="utf-8")
        self.assertRegex(source, r'body\s*=\s*style\([^\n]+fontSize=10[,)]')
        self.assertRegex(source, r'small\s*=\s*style\([^\n]+fontSize=9[,)]')
        self.assertNotIn('p("•", bullet_mark)', source)
        self.assertIn('p("-", bullet_mark)', source)
        with pdfplumber.open(FINAL_PDF) as pdf:
            sizes = [float(char["size"]) for char in pdf.pages[0].chars if char.get("text", "").strip()]
        self.assertGreaterEqual(min(sizes), 7.5)

    def test_content_visually_fills_the_page(self):
        with pdfplumber.open(FINAL_PDF) as pdf:
            words = pdf.pages[0].extract_words()
        education_words = [word for word in words if word["text"] == "建筑学本科"]
        self.assertEqual(len(education_words), 1)
        self.assertGreaterEqual(float(education_words[0]["bottom"]), 690)
        self.assertLessEqual(float(education_words[0]["bottom"]), 760)

    def test_resume_lists_ai_coding_tools(self):
        self.assertIn("Cursor", self.text)
        self.assertIn("OpenAI Codex", self.text)

    def test_public_links_are_clickable(self):
        annotations = self.reader.pages[0].get("/Annots") or []
        uris = []
        for annotation in annotations:
            action = annotation.get_object().get("/A")
            if action and action.get("/URI"):
                uris.append(str(action["/URI"]))
        for expected in (
            "mailto:poeticarch@163.com",
            "https://github.com/dafu110",
            "https://dafu110.github.io/agent-portfolio/",
        ):
            self.assertIn(expected, uris)

    def test_resume_copy_avoids_internal_evaluation_jargon(self):
        for jargon in ("fixture", "holdout", "黄金轨迹"):
            self.assertNotIn(jargon, self.text)
        self.assertIsNone(re.search(r"�|锟斤拷", self.text))


if __name__ == "__main__":
    unittest.main()
