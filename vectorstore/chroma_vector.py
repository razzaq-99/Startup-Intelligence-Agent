from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os

# ---------------------- ChromaDB Vector Store Functions ----------------------

def get_vectorstore():
    """Initialize ChromaDB vector store with Ollama embeddings"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    persist_directory = "./chroma_db"
    
    return Chroma(
        collection_name="startup_vectors",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )

def search_vectorstore(query, k=5):
    """Search the vector store for relevant documents"""
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=k)
    return docs