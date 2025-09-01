import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


load_dotenv()


PITCH_PROMPT = """Create a concise startup pitch outline based on the research:

**Elevator Pitch** (1 sentence)
**Problem & Solution** (2-3 bullets each)
**Market & Customers** (TAM/SAM estimates if available)
**Business Model** (pricing approach)
**Competitors** (top 3 with differentiation)
**Go-to-Market** (first 6 months)
**Financial Ask** (funding amount + use of funds)
**6-Slide Deck Outline** (bullet points per slide)

Research: {research}
Summary: {summary}

Keep each section concise and actionable."""


def generate_pitch(research: str, summary: str) -> str:
    model_name = os.getenv("OLLAMA_MODEL", "gemma:2b")
    temp = float(os.getenv("PITCH_TEMPERATURE", "0"))
    
    llm = ChatOllama(model=model_name, temperature=temp)
    prompt = PromptTemplate.from_template(PITCH_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        # invoke avoids deprecated Chain.run in newer LangChain versions
        out = chain.invoke({"research": research, "summary": summary})
        
        # Handle different output formats from LangChain
        if isinstance(out, dict) and 'text' in out:
            return out['text']
        elif isinstance(out, dict) and 'content' in out:
            return out['content']
        elif isinstance(out, str):
            return out
        else:
            # Convert any other format to string
            return str(out)
            
    except Exception as e:
        print(f"⚠️ Pitch generator LLM failed: {e}")
        # Fallback pitch if LLM fails
        return f"Startup Pitch Outline:\n\n**Problem**: Address market need\n**Solution**: Innovative approach\n**Market**: Target customer segment\n**Business Model**: Revenue streams\n**Competition**: Key differentiators\n**Go-to-Market**: Launch strategy\n**Funding**: Investment ask and use of funds"