from PIL import Image
from utils.ocr_utils import ocr_image


def is_chart_image(pil_img):
    # naive heuristic: if image has many colored regions and lines, assume chart
    try:
        img = pil_img.convert('L')
        extrema = img.getextrema()
        return True if extrema[0] < 10 and extrema[1] > 245 else False
    except Exception:
        return False


def chart_extractor(state):
    # look for image blocks in document_json pages and attempt to extract legend/labels
    doc = state.get('document_json', {})
    charts = []
    pages = doc.get('pages', [])
    for p in pages:
        for block in p.get('blocks', []):
            if block.get('type') == 'image':
                # if OCR text is short, try to mark as chart candidate
                ocr_text = block.get('ocr_text','')
                if ocr_text and len(ocr_text) < 100:
                    charts.append({'page': p.get('page_number'), 'legend': ocr_text})
    state['document_json'] = doc
    state['document_json']['charts'] = charts
    return state
