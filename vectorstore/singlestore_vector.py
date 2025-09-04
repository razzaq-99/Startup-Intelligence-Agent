# vectorstore/singlestore_vector.py
"""
Local vectorstore factory:
- Prefer importing Chroma from the new langchain_chroma package (avoids deprecation warnings).
- Fallback to langchain.vectorstores.Chroma if necessary.
- FAISS fallback if Chroma not available.
"""

import os
import logging
from dotenv import load_dotenv
import warnings

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# reduce noise: try to suppress LangChain-specific deprecation warnings if available
try:
    from langchain import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
except Exception:
    warnings.filterwarnings("ignore", category=DeprecationWarning)

# embeddings - Ollama
try:
    from langchain_ollama import OllamaEmbeddings
except Exception:
    OllamaEmbeddings = None
    logger.info("langchain_ollama not installed; provide another embedding provider or install it.")

# Try to import Chroma from the new package first (avoid deprecation warning)
ChromaClass = None
try:
    from langchain_chroma import Chroma as ChromaClass
except Exception:
    try:
        from langchain.vectorstores import Chroma as ChromaClass
    except Exception:
        ChromaClass = None

# FAISS fallback
FAISSClass = None
try:
    from langchain.vectorstores import FAISS as FAISSClass
except Exception:
    FAISSClass = None

# ---------------------- Vector Store Factory Function ----------------------

def get_vectorstore(persist_directory: str | None = None, collection_name: str = "startup_vectors"):
    persist_directory = persist_directory or os.environ.get("VECTOR_DIR", "./data/chroma_db")
    os.makedirs(persist_directory, exist_ok=True)

    if OllamaEmbeddings is None:
        raise RuntimeError("OllamaEmbeddings not available. Install langchain_ollama or change embedding provider.")

    embeddings = OllamaEmbeddings(model=os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text"))

    # try Chroma new package first
    if ChromaClass is not None:
        try:
            logger.info(f"Using Chroma vectorstore at {persist_directory}, collection: {collection_name}")
            vs = ChromaClass(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embeddings)
            return vs
        except Exception:
            logger.exception("Chroma (preferred) init failed; trying FAISS fallback.")

    if FAISSClass is not None:
        try:
            logger.info("Using FAISS in-memory vectorstore (non-persistent).")
            return FAISSClass.from_texts([], embedding=embeddings)
        except Exception:
            logger.exception("FAISS init failed.")

    raise RuntimeError("No supported local vectorstore found. Install langchain_chroma/chromadb or faiss-cpu and langchain bindings.")
