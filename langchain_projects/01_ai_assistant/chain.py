from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Qwen LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful AI assistant.

        Give simple and clear answers.
        If explaining a technical concept:
        1. Give a definition
        2. Give a simple example
        3. Give a real-world analogy
        """
    ),
    (
        "human",
        "{question}"
    )
])


# Output parser
parser = StrOutputParser()


# LangChain Expression Language
chain = prompt | llm | parser


def ask_ai(question):

    response = chain.invoke({
        "question": question
    })

    return response