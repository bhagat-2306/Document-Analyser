import pdfplumber
from PIL import Image
from utils.ocr_utils import ocr_image


def layout_ocr(state):
    """Produce simple layout blocks per page: text blocks and image blocks with OCR."""
    path = state.get("file_path")
    if not path:
        return state

    doc = pdfplumber.open(path)
    pages = []

    for p_index, page in enumerate(doc.pages, start=1):
        page_obj = {"page_number": p_index, "blocks": []}

        # text blocks using extract_words grouped roughly by top coordinate
        words = page.extract_words()
        if words:
            # naive grouping: join words by line
            lines = {}
            for w in words:
                top = int(w.get('top', 0))
                lines.setdefault(top, []).append(w.get('text', ''))
            for top in sorted(lines.keys()):
                text = ' '.join(lines[top]).strip()
                if text:
                    page_obj['blocks'].append({'type': 'text', 'text': text})

        # images on page
        if page.images:
            for img_index, img in enumerate(page.images, start=1):
                try:
                    # crop the image from page
                    bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                    pil_img = page.within_bbox(bbox).to_image(resolution=150).original
                    ocr_txt = ocr_image(pil_img)
                    page_obj['blocks'].append({'type': 'image', 'ocr_text': ocr_txt})
                except Exception:
                    continue

        pages.append(page_obj)

    state['document_json'] = state.get('document_json', {})
    state['document_json']['pages'] = pages
    return state
