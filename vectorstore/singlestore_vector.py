from langchain_singlestore.vectorstores import SingleStoreVectorStore
from langchain_ollama import OllamaEmbeddings
import os

def get_vectorstore():
    embeddings = OllamaEmbeddings(model="gemma:2b")
    return SingleStoreVectorStore(
        embedding=embeddings,
        host=os.environ["SINGLESTORE_HOST"],
        table_name="startup_vectors"
    )