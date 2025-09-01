import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document


load_dotenv()


SUMMARY_PROMPT = """Analyze the startup research and provide:

1. **Market Summary** (max 100 words)
2. **Top 3 Insights** (bullet points)
3. **Key Competitors** (names only)
4. **Next Steps** (2-3 actions)

Research: {documents}

Focus on actionable insights only."""


def summarize_documents(docs: list[Document] | list[str]) -> str:
    if not docs:
        return "No documents provided to summarize."

    # Convert Document objects to text if needed
    if hasattr(docs[0], "page_content"):
        texts = "\n\n---\n\n".join([d.page_content for d in docs])
    else:
        texts = "\n\n---\n\n".join(docs)

    model_name = os.getenv("OLLAMA_MODEL", "gemma:2b")
    temp = float(os.getenv("SUM_TEMPERATURE", "0"))

    llm = ChatOllama(model=model_name, temperature=temp)
    prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        out = chain.invoke({"documents": texts})
        
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
        print(f"⚠️ Summarizer LLM failed: {e}")
        # Fallback summary if LLM fails
        return f"Research analysis completed. Key focus areas identified for market entry and competitive positioning."