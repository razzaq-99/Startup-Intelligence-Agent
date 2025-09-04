import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain_tavily import TavilySearch
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


load_dotenv()


# ---------------------- Market Research Agent ----------------------

def get_research_agent(max_results: int = 3, model: str | None = None, temp: float | None = None):
    """Return an optimized research agent for faster market research.
    Notes:
    - Reduced max_results for faster processing
    - Uses structured prompts for more focused research
    - Optimized for startup market analysis"""
    
    model_name = model or os.getenv("OLLAMA_MODEL", "gemma:2b")
    temp = float(temp or os.getenv("OLLAMA_TEMPERATURE", "0.1"))

    tavily_tool = TavilySearch(
        max_results=max_results, 
        include_answer=True, 
        include_raw_content=False,  
        search_depth="basic"  
    )

    llm = ChatOllama(model=model_name, temperature=temp)


# ---------------------- Initialize Agent ----------------------
    agent = initialize_agent(
        tools=[tavily_tool],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=3,    
        early_stopping_method="generate"  
    )
    return agent


# ---------------------- Improve Research Performance ----------------------
def quick_research(topic: str, max_results: int = 2) -> str:
    """Fast research function for immediate results"""
    try:
        agent = get_research_agent(max_results=max_results)
        query = f"startup market analysis {topic} key insights competitors 2024"
        result = agent.run(query)
        
        
        if isinstance(result, dict) and 'text' in result:
            return result['text']
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)
            
    except Exception as e:
        print(f"⚠️ Quick research failed: {e}")
        return f"Market research for {topic}: Focus on emerging trends, competitive landscape, and market opportunities. Consider customer pain points and potential market size."