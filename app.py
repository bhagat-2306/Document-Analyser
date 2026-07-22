from pathlib import Path

import streamlit as st
import time

from graph import build_document_graph, run_query_graph
from graph.state import DocumentState

st.set_page_config(page_title='Document Intelligence', page_icon='💡')

st.title('Document Intelligence')
st.write('Upload a document or choose a sample document, then process it once and ask multiple questions.')


def initialize_state() -> DocumentState:
    return {
        'uploaded_file': None,
        'file_path': '',
        'file_type': '',
        'raw_text': '',
        'cleaned_text': '',
        'metadata': {},
        'chunks': [],
        'vectorstore': None,
        'question': '',
        'retrieved_context': '',
        'answer': '',
        'document_json': {},
        'document_context': '',
        'qa_history': [],
        'memory': {}
    }


if 'document_state' not in st.session_state:
    st.session_state.document_state = initialize_state()
    st.session_state.source_file = None
    st.session_state.processed = False

with st.sidebar:
    st.header('Document Source')

    uploaded_file = st.file_uploader(
        'Upload a document',
        type=['pdf', 'docx', 'xlsx', 'xls', 'png', 'jpg', 'jpeg'],
        key='uploaded_file'
    )

    process_button = st.button('Process document')

    if process_button:
        if uploaded_file is None:
            st.warning('Please upload a document.')
        else:
            state = initialize_state()
            state['uploaded_file'] = uploaded_file
            with st.spinner('Processing document...'):
                st.session_state.document_state = build_document_graph(state)
                st.session_state.source_file = uploaded_file.name
                st.session_state.processed = True
                st.success('Document processed successfully. You can now ask questions against it.')

    def _safe_rerun():
        rerun = getattr(st, 'experimental_rerun', None)
        if callable(rerun):
            try:
                rerun()
                return
            except Exception:
                pass
        # fallback: clear session and stop
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        # attempt to nudge client by changing query params if available
        if hasattr(st, 'experimental_set_query_params'):
            try:
                st.experimental_set_query_params(_reset=int(time.time()))
            except Exception:
                pass
        st.stop()

    if st.button('Reset session'):
        st.session_state.document_state = initialize_state()
        st.session_state.source_file = None
        st.session_state.processed = False
        if 'uploaded_file' in st.session_state:
            st.session_state.uploaded_file = None
        _safe_rerun()

if st.session_state.processed:
    state = st.session_state.document_state

    st.success('Document processed successfully.')
    st.markdown(f'**Source:** {st.session_state.source_file}')
    st.write('The uploaded document has been processed and is ready for question answering.')

    question = st.text_input('Ask a question about this document', key='document_question')

    if st.button('Ask question'):
        if not question:
            st.warning('Please type a question before asking.')
        else:
            with st.spinner('Generating answer...'):
                st.session_state.document_state = run_query_graph(state, question)
                st.success('Answer generated.')

    if state.get('answer'):
        st.subheader('Answer')
        st.write(state['answer'])
else:
    st.info('Upload or select a document and click Process document to start.')
