try:
    import camelot
    _HAS_CAMELOT = True
except Exception:
    _HAS_CAMELOT = False

import pdfplumber


def table_extractor(state):
    path = state.get('file_path')
    tables_out = []
    if not path:
        state['document_json'] = state.get('document_json', {})
        state['document_json']['tables'] = tables_out
        return state

    if _HAS_CAMELOT:
        try:
            tables = camelot.read_pdf(path, pages='all')
            for t in tables:
                tables_out.append({'data': t.df.values.tolist(), 'shape': t.df.shape})
        except Exception:
            pass

    # fallback using pdfplumber
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                for tbl in page.extract_tables():
                    tables_out.append({'data': tbl})
    except Exception:
        pass

    state['document_json'] = state.get('document_json', {})
    state['document_json']['tables'] = tables_out
    return state
