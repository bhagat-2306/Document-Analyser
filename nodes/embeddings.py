from langchain_community.vectorstores import FAISS

from models.embedding_model import embedding_model


def embeddings(state):

    vectorstore = FAISS.from_texts(
        texts=state["chunks"],
        embedding=embedding_model
    )

    state["vectorstore"] = vectorstore

    return state