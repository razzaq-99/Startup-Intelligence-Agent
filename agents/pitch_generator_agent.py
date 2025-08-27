from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_pitch(insights):
    llm = ChatOllama(model="gemma:2b", temperature=0)
    prompt = PromptTemplate.from_template(
        "Using the insights below, generate a pitch outline:\n\n{insights}\n\n"
    )
    chain = LLMChain(prompt=prompt, llm=llm)
    return chain.run(insights)