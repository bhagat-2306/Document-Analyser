import fitz
from PIL import Image

from utils.ocr_utils import ocr_image


def extract_pdf(state):
    path = state["file_path"]
    doc = fitz.open(path)

    text = ""

    for page_index, page in enumerate(doc, start=1):
        text += f"\n=== Page {page_index} ===\n"

        page_text = page.get_text("text") or ""
        if page_text.strip():
            text += page_text.strip() + "\n"
        else:
            text += "[No extracted text detected on this page.]\n"

        pix = page.get_pixmap(dpi=300)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = ocr_image(image)

        if ocr_text.strip():
            text += "\n[OCR text from page image]\n"
            text += ocr_text.strip() + "\n"

    state["raw_text"] = text
    return state