from vectorstore.chroma_vector import get_vectorstore

def store_documents(docs):
    """Store documents in ChromaDB vector store"""
    vs = get_vectorstore()
    vs.add_documents(docs)
    return f"Stored {len(docs)} documents in vector database"

def search_documents(query, k=5):
    """Search for relevant documents in the vector store"""
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=k)
    return docs