from typing import List

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate


class QueryExpander:

    def __init__(self, temperature: float = 0):

        self.llm = ChatOllama(
            model="llama3.2",
            temperature=temperature
        )

        self.query_expansion_prompt = PromptTemplate(
            input_variables=["question"],
            template="""
Given the following question, generate 3 different versions of the question
that capture different aspects and perspectives of the original question.

Make the variations semantically diverse but relevant.

Original Question:
{question}

Generate variations in the following format:

1. [First variation]
2. [Second variation]
3. [Third variation]

Only output the numbered variations, nothing else.
"""
        )

    def expand_query(self, question: str) -> List[str]:

        try:

            response = self.llm.invoke(
                self.query_expansion_prompt.format(
                    question=question
                )
            )

            variations = []

            for line in response.content.strip().splitlines():

                line = line.strip()

                if ". " in line:
                    variations.append(
                        line.split(". ", 1)[1].strip()
                    )

            # Add original question
            variations.append(question)

            return variations

        except Exception as e:

            print(f"Error in query expansion: {e}")

            # Fallback to original query
            return [question]


def main():

    expander = QueryExpander()

    questions = [
        "What are the main causes of global warming?",
        "How does exercise affect mental health?",
        "What are the benefits of renewable energy?",
    ]

    for original_question in questions:

        print("\n" + "=" * 60)

        print(f"Original Question:")
        print(original_question)

        print("\nExpanded Queries:")

        expanded_queries = expander.expand_query(
            original_question
        )

        for i, query in enumerate(expanded_queries, 1):

            print(f"{i}. {query}")


if __name__ == "__main__":
    main()

# output

# ============================================================
# Original Question:
# What are the main causes of global warming?

# Expanded Queries:
# 1. What are the primary factors contributing to the acceleration of global warming, and how do they interact with one another?
# 2. From a historical perspective, what were the key events and decisions that led to the current state of global warming, and how have they impacted the planet's climate?
# 3. What are the most significant greenhouse gas emissions sources, and how do they vary across different regions and industries, in relation to global warming mitigation strategies?
# 4. What are the main causes of global warming?

# ============================================================
# Original Question:
# How does exercise affect mental health?

# Expanded Queries:
# 1. What role do physical exercise and sedentary behavior play in the development and management of mental health disorders?
# 2. How do different types and intensities of exercise impact mood, anxiety, and depression in individuals with varying levels of physical activity?
# 3. Can exercise be a therapeutic tool for mitigating symptoms of mental health conditions, and if so, what are the most effective exercise programs and strategies for promoting mental well-being?
# 4. How does exercise affect mental health?

# ============================================================
# Original Question:
# What are the benefits of renewable energy?

# Expanded Queries:
# 1. How do renewable energy sources impact global climate change mitigation strategies?
# 2. What are the economic incentives for transitioning to renewable energy sources in developing countries?
# 3. How do the social and cultural implications of renewable energy adoption influence community development and social equity?
# 4. What are the benefits of renewable energy?    