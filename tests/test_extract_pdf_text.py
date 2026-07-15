import tempfile
import unittest
from importlib.util import find_spec
from pathlib import Path

from extract_pdf_text import extract_pdf_text


class ExtractPdfTextTests(unittest.TestCase):
    def test_rejects_missing_pdf_with_clear_path(self):
        missing = Path(tempfile.gettempdir()) / "missing-resume.pdf"
        with self.assertRaisesRegex(FileNotFoundError, "missing-resume.pdf"):
            extract_pdf_text(missing)

    def test_rejects_non_pdf_input(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as handle:
            with self.assertRaisesRegex(ValueError, "Expected a .pdf"):
                extract_pdf_text(Path(handle.name))

    @unittest.skipIf(find_spec("pdfplumber") is None, "pdfplumber is not installed")
    def test_extracts_the_public_resume(self):
        pages = extract_pdf_text(Path(__file__).resolve().parents[1] / "assets" / "resume.pdf")
        self.assertEqual(len(pages), 1)
        self.assertIn("傅孟涵", pages[0])


if __name__ == "__main__":
    unittest.main()
