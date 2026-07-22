from typing import TypedDict, Dict, Any, List


class DocumentState(TypedDict):

    uploaded_file: Any

    file_path: str

    file_type: str

    raw_text: str

    cleaned_text: str

    metadata: Dict

    chunks: List[str]

    vectorstore: Any

    question: str

    retrieved_context: str

    answer: str
    # structured multimodal document representation
    document_json: Dict
    # QA history for the current document — list of {question, answer}
    qa_history: List[Dict[str, str]]
    # simple memory store (persisted for the session)
    memory: Dict[str, Any]


# Backwards compatibility: some modules may still import `InvoiceState`
InvoiceState = DocumentState