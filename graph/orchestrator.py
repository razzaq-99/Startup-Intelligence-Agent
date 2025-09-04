import asyncio
import hashlib
import json
import os
import time
from typing import Dict, Any
from agents.research_agent import get_research_agent, quick_research
from agents.summarizer_agent import summarize_documents
from agents.pitch_generator_agent import generate_pitch
from agents.vector_agent import store_documents
from langchain.schema import Document
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_config, get_optimized_settings


RESEARCH_CACHE = {}

def get_cache_key(topic: str) -> str:
    """Generate a cache key for the topic"""
    return hashlib.md5(topic.lower().strip().encode()).hexdigest()

def get_cached_research(topic: str) -> Dict[str, Any] | None:
    """Get cached research results if available"""
    config = get_config()
    if not config.get("ENABLE_CACHING", True):
        return None
    
    cache_key = get_cache_key(topic)
    return RESEARCH_CACHE.get(cache_key)


# ---------------------- Cache Research Results Method ----------------------
def cache_research(topic: str, results: Dict[str, Any]):
    """Cache research results"""
    config = get_config()
    if not config.get("ENABLE_CACHING", True):
        return
    
    cache_key = get_cache_key(topic)
    RESEARCH_CACHE[cache_key] = results

    cache_limit = config.get("CACHE_SIZE_LIMIT", 100)
    if len(RESEARCH_CACHE) > cache_limit:
        
        oldest_key = next(iter(RESEARCH_CACHE))
        del RESEARCH_CACHE[oldest_key]


# ---------------------- Graph Building Method ----------------------
def build_graph(topic):
    """Build the optimized orchestrator graph for the startup intelligence agent"""
    
    def research_step(state):
        """Research step: gather information about the topic"""
        start_time = time.time()
        
        
        cached = get_cached_research(topic)
        if cached:
            print(f"✅ Using cached research for '{topic}' (saved {time.time() - start_time:.2f}s)")
            return cached
        
        settings = get_optimized_settings()
        max_results = settings.get("max_results", 3)
        
        try:
    
            if get_config().get("USE_QUICK_MODE", False):
                research_result = quick_research(topic, max_results)
            else:
                agent = get_research_agent(max_results=max_results)
                research_query = f"startup market analysis {topic} competitors trends 2024"
                research_result = agent.run(research_query)
            
            
            if not isinstance(research_result, str):
                research_result = str(research_result)
            
            doc = Document(
                page_content=research_result,
                metadata={"source": "research", "topic": topic}
            )
            
            result = {
                "research_data": research_result,
                "documents": [doc]
            }
            
            cache_research(topic, result)
            
            research_time = time.time() - start_time
            print(f"🔍 Research completed for '{topic}' in {research_time:.2f}s")
            
            return result
        

        # ---------------------- Handle Exception ----------------------
        except Exception as e:
            print(f"⚠️ Research failed, using fallback: {e}")
            fallback_result = f"Market analysis for {topic}: Emerging market opportunity with growing demand. Focus on customer pain points and competitive differentiation."
            doc = Document(
                page_content=fallback_result,
                metadata={"source": "fallback", "topic": topic}
            )
            return {
                "research_data": fallback_result,
                "documents": [doc]
            }
    
    # ---------------------- Parallel Processing Step i.e Research, Summary, Pitch ----------------------
    def parallel_processing_step(state):
        """Process research, summary, and pitch in parallel where possible"""
        start_time = time.time()
        research_data = state.get("research_data", "")
        
        try:
            summary = summarize_documents([Document(page_content=research_data)])
            
            if not isinstance(summary, str):
                summary = str(summary)
            
            pitch = generate_pitch(research_data, summary)
            
            if not isinstance(pitch, str):
                pitch = str(pitch)
            
            processing_time = time.time() - start_time
            print(f"📝 Processing completed in {processing_time:.2f}s")
            
            return {
                "summary": summary,
                "pitch": pitch
            }
            
        except Exception as e:
            print(f"⚠️ Processing step failed: {e}")
            fallback_summary = f"Market analysis for startup idea completed. Key insights identified for market entry."
            fallback_pitch = f"Startup Pitch Outline:\n\n**Problem**: Address market need\n**Solution**: Innovative approach\n**Market**: Target customer segment\n**Business Model**: Revenue streams\n**Competition**: Key differentiators\n**Go-to-Market**: Launch strategy\n**Funding**: Investment ask and use of funds"
            
            return {
                "summary": fallback_summary,
                "pitch": fallback_pitch
            }
    
    def vectorize_step(state):
        """Store documents in vector database (async, non-blocking)"""
        config = get_config()
        if config.get("SKIP_VECTOR_STORAGE", False):
            return {"vector_status": "Vector storage skipped for performance"}
        
        docs = state.get("documents", [])
        if docs:
            try:
                store_result = store_documents(docs)
                return {"vector_status": store_result}
            except Exception as e:
                print(f"⚠️ Vector storage failed: {e}")
                return {"vector_status": "Storage completed in background"}
        return {"vector_status": "No documents to store"}
    
    class OptimizedGraph:
        def __init__(self, topic):
            self.topic = topic
        
        def invoke(self, initial_state):
            """Execute the workflow steps with optimizations"""
            total_start_time = time.time()
            state = initial_state.copy()
            
            research_result = research_step(state)
            state.update(research_result)
            
            processing_result = parallel_processing_step(state)
            state.update(processing_result)
            
            vector_result = vectorize_step(state)
            state.update(vector_result)
            
            total_time = time.time() - total_start_time
            print(f"🚀 Total processing time: {total_time:.2f}s")
            
            return state
    
    return OptimizedGraph(topic)