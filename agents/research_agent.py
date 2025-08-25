from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import initialize_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

def get_research_agent():
    search_tool = TavilySearchResults()
    tools = [search_tool]

    llm = ChatOllama(model="gemma:2b", temperature=0)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    return agent