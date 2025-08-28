from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama

def summarize_documents(docs):

    llm = ChatOllama(model="gemma:2b", temperature=0)
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)