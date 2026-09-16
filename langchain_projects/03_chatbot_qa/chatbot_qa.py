import os
from typing import List, Dict, Tuple

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import SeleniumURLLoader

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = "qwen2.5:3b"

EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_NUM_GPU = int(os.getenv("OLLAMA_EMBEDDING_NUM_GPU", "0"))


URLS = [
    "https://beebom.com/what-is-nft-explained/",
    "https://beebom.com/how-delete-servers-discord/",
    "https://beebom.com/how-list-groups-linux/",
    "https://beebom.com/how-open-port-linux/",
    "https://beebom.com/linux-vs-windows/",
]
def scrape_documents(urls: List[str]):
    """
    Load web pages using SeleniumURLLoader.
    """

    print("\n" + "=" * 60)
    print("SCRAPING DOCUMENTS")
    print("=" * 60)

    try:
        loader = SeleniumURLLoader(urls=urls)
        documents = loader.load()
        print(f"\nSuccessfully loaded: {len(documents)} documents")
        for i,document in enumerate(documents, start=1):
            source = document.metadata.get(
                "source",
                "Unknown source"
            )
            content_length = len(document.page_content)
            print(
                f"{i}. {source} "
                f"({content_length} characters)"
            )

        return documents

    except Exception as e:

        print("\nError while scraping:")
        print(e)

        return []


def split_documents(documents) -> Tuple[List[str], List[Dict]]:

    print("\n" + "=" * 60)
    print("SPLITTING DOCUMENTS")
    print("=" * 60)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    texts = []
    metadatas = []

    for document in documents:
        text = document.page_content
        source = document.metadata.get(
            "source",
            "Unknown"
        )
        chunks = text_splitter.split_text(text)

        for chunk in chunks:
            if chunk.strip():
                texts.append(chunk)
                metadatas.append({
                    "source": source
                })

    print(f"\nCreated {len(texts)} chunks")
    return texts, metadatas

def test_embedding_model():

    print("\n" + "=" * 60)
    print("TESTING EMBEDDING MODEL")
    print("=" * 60)
    print(f"Model: {EMBEDDING_MODEL}")

    try:
        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            num_gpu=EMBEDDING_NUM_GPU,
            validate_model_on_init=True,
        )
        test_text = [
            "This is a test sentence for embeddings."
        ]
        vectors = embeddings.embed_documents(
            test_text
        )
        print("\nEmbedding test successful!")
        print(
            f"Embedding dimension: {len(vectors[0])}"
        )

        return embeddings

    except Exception as e:

        print("\nEmbedding model FAILED.")
        print("\nError:")
        print(e)

        print("\nMake sure Ollama is running:")
        print("ollama serve")

        print("\nAnd make sure the model exists:")
        print(f"ollama pull {EMBEDDING_MODEL}")
        print(
            "\nIf Ollama reports that its server process aborted, keep "
            "OLLAMA_EMBEDDING_NUM_GPU=0 (the default), restart Ollama, "
            "and try again."
        )

        raise

def create_vector_store(
    texts: List[str],
    metadatas: List[Dict],
    embeddings
):

    print("\n" + "=" * 60)
    print("CREATING CHROMA VECTOR STORE")
    print("=" * 60)

    try:

        db = Chroma.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=embeddings,
            collection_name="beebom_rag"
        )

        print("\nChroma vector store created successfully.")

        return db

    except Exception as e:

        print("\nError creating Chroma database:")
        print(e)

        raise

def setup_qa_chain(db):

    print("\n" + "=" * 60)
    print("SETTING UP QA CHAIN")
    print("=" * 60)

    # LLM
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0
    )

    # Retriever
    retriever = db.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful RAG assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, clearly say:

"I don't have enough information in the provided documents."

Do not invent information.

Keep the answer clear, concise, and useful.

### Context
{context}
### Question
{question}
### Answer
"""
    )
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("QA chain ready.")
    return chain, retriever

def process_query(
    chain,
    retriever,
    query: str
):

    try:

        # Generate answer
        answer = chain.invoke(query)
        # Retrieve source documents
        documents = retriever.invoke(query)
        sources = []
        for document in documents:
            source = document.metadata.get(
                "source",
                "Unknown"
            )

            if source not in sources:
                sources.append(source)

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        print("\nError processing query:")
        print(e)

        return {
            "answer": "An error occurred while processing your question.",
            "sources": []
        }

def main():

    print("\n")
    print("=" * 60)
    print("WEB RAG ASSISTANT")
    print("=" * 60)
    embeddings = test_embedding_model()
    documents = scrape_documents(URLS)

    if not documents:
        print("\nNo documents were loaded.")
        return

    texts, metadatas = split_documents(
        documents
    )

    if not texts:
        print("\nNo text chunks were created.")
        return

    
    db = create_vector_store(
        texts,
        metadatas,
        embeddings
    )

    
    chain, retriever = setup_qa_chain(db)

    
    print("\n" + "=" * 60)
    print("RAG ASSISTANT READY")
    print("=" * 60)

    print("\nType 'quit' to exit.")

    while True:

        query = input(
            "\nEnter your question: "
        ).strip()

        if not query:
            continue

        if query.lower() == "quit":
            print("\nGoodbye!")
            break

        result = process_query(
            chain,
            retriever,
            query
        )

        print("\n" + "-" * 60)

        print("ANSWER")
        print("-" * 60)

        print(result["answer"])

        if result["sources"]:

            print("\n" + "-" * 60)

            print("SOURCES")
            print("-" * 60)

            for source in result["sources"]:

                print(f"- {source}")


if __name__ == "__main__":
    main()
