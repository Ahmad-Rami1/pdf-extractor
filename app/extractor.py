from pathlib import Path
from typing import List
import pdfplumber, pytesseract, tempfile, subprocess
from pdf2image import convert_from_path

TESS_LANGS = "deu+eng"

def _is_scanned(page) -> bool:
    """Heuristic: if pdfplumber extract_text() returns None or very short."""
    txt = page.extract_text()
    return txt is None or len(txt.strip()) < 20

def extract_text(pdf_path: Path) -> str:
    """Return full doc text, OCR-ing scanned pages."""
    out: List[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            if _is_scanned(page):
                # rasterise single page to image and OCR it
                with tempfile.TemporaryDirectory() as tmp:
                    images = convert_from_path(
                        pdf_path,
                        dpi=300,
                        first_page=idx,
                        last_page=idx,
                        output_folder=tmp,
                        fmt="png"
                    )
                    ocr_txt = "\n".join(
                        pytesseract.image_to_string(im, lang=TESS_LANGS)
                        for im in images
                    )
                    out.append(ocr_txt)
            else:
                out.append(page.extract_text())
    return "\n".join(out)