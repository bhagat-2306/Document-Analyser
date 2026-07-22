import json


def structure_document(state):
    # assemble a higher-level document JSON combining metadata, text, tables, charts
    doc = state.get('document_json', {})
    assembled = {
        'metadata': state.get('metadata', {}),
        'pages': doc.get('pages', []),
        'tables': doc.get('tables', []),
        'charts': doc.get('charts', []),
        'cleaned_text': state.get('cleaned_text', ''),
    }

    state['document_json'] = assembled
    # also provide a compact context string for retrieval/llm
    state['document_context'] = json.dumps(assembled, ensure_ascii=False)
    return state
