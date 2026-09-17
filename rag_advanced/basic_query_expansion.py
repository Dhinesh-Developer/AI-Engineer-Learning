from typing import List

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate


class QueryExpander:

    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0
        )

        self.prompt = PromptTemplate(
            input_variables=["question"],
            template="""
Generate 3 different search queries for the user's question.

The queries must:
- have the same intent
- use different wording
- cover different aspects

Original question:
{question}

Return exactly:

1. query
2. query
3. query
"""
        )

    def expand(self, question: str) -> List[str]:
        response = self.llm.invoke(
            self.prompt.format(question=question)
        )

        queries = []
        for line in response.content.splitlines():
            line = line.strip()

            if ". " in line:
                query = line.split(". ", 1)[1]
                queries.append(query)

        queries.append(question)
        return queries


if __name__ == "__main__":

    expander = QueryExpander()
    question = "How does exercise improve mental health?"
    queries = expander.expand(question)
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")

# 1. "Benefits of physical activity on mental well-being"
# 2. "How exercise affects mental health outcomes"
# 3. "The relationship between physical exercise and mental health benefits"
# 4. How does exercise improve mental health?        