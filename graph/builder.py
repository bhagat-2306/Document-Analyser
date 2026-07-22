from graph.state import InvoiceState
from graph.router import route_document
from nodes.chunk import chunk
from nodes.detect_filetype import detect_filetype
from nodes.embeddings import embeddings
from nodes.extract_docx import extract_docx
from nodes.extract_excel import extract_excel
from nodes.extract_image import extract_image
from nodes.extract_pdf import extract_pdf
from nodes.load_document import load_document
from nodes.metadata import metadata
from nodes.preprocess import preprocess

EXTRACTORS = {
    'pdf': extract_pdf,
    'docx': extract_docx,
    'excel': extract_excel,
    'image': extract_image,
}


def build_document_graph(state: InvoiceState) -> InvoiceState:
    state = load_document(state)
    state = detect_filetype(state)

    route = route_document(state)
    extractor = EXTRACTORS.get(route)
    if extractor is None:
        raise ValueError(f'Unsupported extraction route: {route}')

    state = extractor(state)
    state = preprocess(state)
    state = metadata(state)
    state = chunk(state)
    state = embeddings(state)
    return state
