from agents.research_agent import get_research_agent
from agents.summarizer_agent import summarize_documents
from agents.pitch_generator_agent import generate_pitch
from agents.vector_agent import store_documents
from langchain.schema import Document

def build_graph(topic):
    """Build the orchestrator graph for the startup intelligence agent"""
    
    def research_step(state):
        """Research step: gather information about the topic"""
        agent = get_research_agent()
        research_query = f"market research startup trends competitors {topic}"
        research_result = agent.run(research_query)
        
        doc = Document(
            page_content=research_result,
            metadata={"source": "research", "topic": topic}
        )
        
        return {
            "research_data": research_result,
            "documents": [doc]
        }
    
    def vectorize_step(state):
        """Store documents in vector database"""
        docs = state.get("documents", [])
        if docs:
            store_result = store_documents(docs)
            return {"vector_status": store_result}
        return {"vector_status": "No documents to store"}
    
    def summarize_step(state):
        """Summarize the research findings"""
        docs = state.get("documents", [])
        if docs:
            summary = summarize_documents(docs)
            return {"summary": summary}
        return {"summary": "No documents to summarize"}
    
    def pitch_step(state):
        """Generate pitch based on insights"""
        summary = state.get("summary", "")
        research_data = state.get("research_data", "")
        
        
        insights = f"Research Data:\n{research_data}\n\nSummary:\n{summary}"
        
        pitch = generate_pitch(insights)
        return {"pitch": pitch}
    
    class SimpleGraph:
        def __init__(self, topic):
            self.topic = topic
        
        def invoke(self, initial_state):
            """Execute the workflow steps sequentially"""
            state = initial_state.copy()
            
            research_result = research_step(state)
            state.update(research_result)
            
            vector_result = vectorize_step(state)
            state.update(vector_result)
            
            summary_result = summarize_step(state)
            state.update(summary_result)
            
            pitch_result = pitch_step(state)
            state.update(pitch_result)
            
            return state
    
    return SimpleGraph(topic)