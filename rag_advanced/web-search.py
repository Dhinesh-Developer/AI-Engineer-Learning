from ddgs import DDGS
from langchain_ollama import ChatOllama

def web_search(query, max_results=5):
    results = DDGS().text(
        query,
        max_results=max_results
    )
    return results

query = "What is RAG in generative AI?"

results = web_search(query=query)

context = ""

for res in results:
    context += f"""
Title: {res.get("title")}
URL: {res.get("href")}
Content: {res.get("body")}
---
"""

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)    

prompt = f"""
Answer the question using the web search results.

Question:
{query}

Search results:
{context}

Answer:
"""

response = llm.invoke(prompt)
print(response.content)


# RAG, or Retrieval-Augmented Generation, is an AI framework that combines the strengths of traditional information retrieval systems with the capabilities of generative large language models (LLMs). This approach allows for more reliable AI answers by integrating the process of searching for relevant information with the generation of a response. 
# RAG extends the already powerful capabilities of LLMs to specific domains or an organization's internal knowledge base, all without the need to retrain the model. This technique was first proposed in 2020 and has since become a widely adopted approach in modern AI systems. By using RAG, LLMs can access internal company data or generate responses based on authoritative sources, making their outputs more accurate and relevant for various tasks such as answering questions, translating languages, and completing sentences.
# RAG is a cost-effective method to improve the output of LLMs, ensuring they remain relevant, accurate, and useful in different contexts. It is particularly useful for applications that require LLMs to be more domain-specific or to access internal knowledge bases.