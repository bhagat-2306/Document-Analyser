from graph.state import DocumentState
from nodes.llm import llm
from nodes.retrieve import retrieve


def run_query_graph(state: DocumentState, question: str) -> DocumentState:
    if state.get('vectorstore') is None:
        raise ValueError('Document must be processed before running a query.')

    state['question'] = question
    state = retrieve(state)
    state = llm(state)
    # append to QA history
    qa = {'question': question, 'answer': state.get('answer', '')}
    history = state.get('qa_history') or []
    history.append(qa)
    state['qa_history'] = history
    return state
