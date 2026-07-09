from langchain_ollama import ChatOllama

llm = ChatOllama(model = "llama3.2")

def ai_env(prompt:str):
    response = llm.invoke(prompt)
    return response.content

