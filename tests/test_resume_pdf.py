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
        headings = ["个人简介", "AI 项目经历", "工作经历", "专业能力", "教育背景"]
        positions = [self.text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        for removed in ("岗位匹配", "背景迁移", "作品验证路径"):
            self.assertNotIn(removed, self.text)

    def test_personal_ai_projects_are_not_listed_as_employment(self):
        work = self.text.split("工作经历", 1)[1].split("专业能力", 1)[0]
        compact_work = re.sub(r"\s+", "", work)
        self.assertNotIn("个人 AI 应用项目实践", work)
        for employer in (
            "中国市政工程华北设计研究总院",
            "北京土人城市规划设计股份有限公司",
            "北京市建筑设计研究院股份有限公司",
            "北京创研建筑设计中心",
        ):
            self.assertIn(employer, compact_work)
        self.assertIn("2023 - 至今", work)
        self.assertIn("2015 - 2017", work)
        self.assertIn("2017 - 2019、2021 - 2023", work)

    def test_resume_leads_with_ai_evidence_and_dates_each_project(self):
        compact_text = re.sub(r"\s+", "", self.text)
        self.assertIn(
            "聚焦企业AI应用产品与解决方案，已独立完成4个可验证工作流原型",
            compact_text,
        )
        self.assertNotIn("现转向", self.text)
        ai_projects = self.text.split("AI 项目经历", 1)[1].split("工作经历", 1)[0]
        self.assertEqual(ai_projects.count("2026.07"), 4)

    def test_resume_uses_current_targeting_and_safe_personal_information(self):
        self.assertIn("北京", self.text)
        self.assertIn("北京 · 可在北京工作 · 随时到岗 · 现场 / 混合 / 远程均可", self.text)
        for private_or_stale in ("34 岁", "男", "15k", "20k", "建筑师、室内设计师"):
            self.assertNotIn(private_or_stale, self.text)

    def test_resume_includes_verified_representative_project_scale(self):
        compact_text = re.sub(r"\s+", "", self.text)
        for evidence in (
            "齐河县国家现代农业产业园综合服务中心",
            "占地5.25万㎡",
            "建筑面积2.9万㎡",
            "外径103.8米",
        ):
            self.assertIn(evidence, compact_text)
        self.assertNotIn("效率提升60%", compact_text)

    def test_resume_includes_second_public_representative_scheme(self):
        compact_text = re.sub(r"\s+", "", self.text)
        for evidence in (
            "乐清市盐盆山清和公园一体化建设工程-山顶建筑设计方案",
            "大赋建筑",
            "3657㎡",
            "方案设计一等奖",
            "大跨度木结构",
        ):
            self.assertIn(evidence, compact_text)
        self.assertEqual(compact_text.count("代表方案"), 2)
        self.assertIn("代表方案01齐河县国家现代农业产业园综合服务中心", compact_text)
        self.assertIn("代表方案02乐清市盐盆山清和公园一体化建设工程-山顶建筑设计方案", compact_text)
        self.assertNotIn("公开项目", compact_text)
        self.assertNotIn("独立设计", compact_text)
        self.assertNotIn("主创", compact_text)

        annotations = self.reader.pages[0].get("/Annots") or []
        uris = []
        for annotation in annotations:
            action = annotation.get_object().get("/A")
            if action and action.get("/URI"):
                uris.append(str(action["/URI"]))
        self.assertFalse(any("xhslink.com" in uri for uri in uris))

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
