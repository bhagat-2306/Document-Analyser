from config import TOP_K


def retrieve(state):
    docs = state['vectorstore'].similarity_search(
        state['question'],
        k=TOP_K,
    )
    state['retrieved_context'] = '\n\n'.join(doc.page_content for doc in docs)
    return state
