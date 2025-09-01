"""
Configuration file for Startup Intelligence Agent performance optimization
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Performance Configuration
PERFORMANCE_CONFIG = {
    # Research settings
    "MAX_RESEARCH_RESULTS": int(os.getenv("MAX_RESEARCH_RESULTS", "3")),
    "RESEARCH_TIMEOUT": int(os.getenv("RESEARCH_TIMEOUT", "30")),
    
    # LLM settings
    "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "gemma:2b"),
    "OLLAMA_TEMPERATURE": float(os.getenv("OLLAMA_TEMPERATURE", "0.1")),
    "OLLAMA_EMBED_MODEL": os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
    
    # Caching settings
    "ENABLE_CACHING": os.getenv("ENABLE_CACHING", "true").lower() == "true",
    "CACHE_SIZE_LIMIT": int(os.getenv("CACHE_SIZE_LIMIT", "100")),
    
    # Vector storage settings
    "VECTOR_STORAGE_ENABLED": os.getenv("VECTOR_STORAGE_ENABLED", "true").lower() == "true",
    "VECTOR_DIR": os.getenv("VECTOR_DIR", "./chroma_db"),
    
    # API settings
    "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
    "TAVILY_SEARCH_DEPTH": os.getenv("TAVILY_SEARCH_DEPTH", "basic"),
    
    # Performance flags
    "ENABLE_PARALLEL_PROCESSING": os.getenv("ENABLE_PARALLEL_PROCESSING", "true").lower() == "true",
    "SKIP_VECTOR_STORAGE": os.getenv("SKIP_VECTOR_STORAGE", "false").lower() == "true",
    "USE_QUICK_MODE": os.getenv("USE_QUICK_MODE", "false").lower() == "true"
}

# Quick mode configuration for faster results
QUICK_MODE_CONFIG = {
    "MAX_RESEARCH_RESULTS": 2,
    "RESEARCH_TIMEOUT": 15,
    "SKIP_VECTOR_STORAGE": True,
    "ENABLE_CACHING": True
}

def get_config():
    """Get the current configuration, applying quick mode if enabled"""
    config = PERFORMANCE_CONFIG.copy()
    
    if config.get("USE_QUICK_MODE", False):
        config.update(QUICK_MODE_CONFIG)
    
    return config

def get_optimized_settings():
    """Get settings optimized for maximum performance"""
    return {
        "max_results": PERFORMANCE_CONFIG["MAX_RESEARCH_RESULTS"],
        "search_depth": PERFORMANCE_CONFIG["TAVILY_SEARCH_DEPTH"],
        "enable_caching": PERFORMANCE_CONFIG["ENABLE_CACHING"],
        "skip_vector_storage": PERFORMANCE_CONFIG["SKIP_VECTOR_STORAGE"]
    } 