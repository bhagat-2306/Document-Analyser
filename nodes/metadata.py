from utils.document_regex import extract_fields


def metadata(state):

    extracted = extract_fields(state["cleaned_text"])

    state["metadata"] = extracted

    return state