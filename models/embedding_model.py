from langchain_community.embeddings import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL


embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)