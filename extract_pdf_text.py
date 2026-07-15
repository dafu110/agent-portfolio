"""Extract readable text from a selected PDF resume."""

from argparse import ArgumentParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_PDF = ROOT / "assets" / "resume.pdf"


def extract_pdf_text(pdf_path: Path, character_limit: int | None = None) -> list[str]:
    """Return page text from *pdf_path* without silently selecting another PDF."""
    path = pdf_path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file: {path}")

    try:
        import pdfplumber
    except ModuleNotFoundError as exc:
        raise RuntimeError("pdfplumber is required; run: python -m pip install -r requirements.txt") from exc

    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    if character_limit is not None:
        pages = [page[:character_limit] for page in pages]
    return pages


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--limit", type=int, default=None, help="maximum characters printed per page")
    args = parser.parse_args()

    pages = extract_pdf_text(args.pdf, args.limit)
    print(f"file: {args.pdf.resolve()}")
    print(f"pages: {len(pages)}")
    for index, page in enumerate(pages, start=1):
        print(f"--- PAGE {index} ---")
        print(page)


if __name__ == "__main__":
    main()
