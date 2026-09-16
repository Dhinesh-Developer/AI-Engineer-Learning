

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_ollama import (
    ChatOllama,
    OllamaEmbeddings
)

from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ============================================================
# CONFIGURATION
# ============================================================

LLM_MODEL = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"

CHROMA_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "pdf_rag"


# ============================================================
# EMBEDDINGS
# ============================================================

embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)


# ============================================================
# LLM
# ============================================================

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=0
)


# ============================================================
# LOAD PDF
# ============================================================

# Replace PyMuPDFLoader import
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    try:
        print(f"Loading PDF: {file_path}")

        # Use PyPDFLoader instead
        loader = PyPDFLoader(file_path)

        documents = loader.load()

        if not documents:
            raise ValueError("PDF contains no readable pages.")

        print(f"Successfully loaded {len(documents)} pages.")
        return documents

    except Exception as error:
        raise RuntimeError(
            f"Failed to load PDF.\n\n"
            f"File: {file_path}\n\n"
            f"Error: {error}"
        ) from error

# ============================================================
# SPLIT DOCUMENT
# ============================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len
    )

    chunks = splitter.split_documents(
        documents
    )

    if not chunks:

        raise ValueError(
            "No chunks were created from the PDF."
        )

    print(
        f"Created {len(chunks)} chunks."
    )

    return chunks


# ============================================================
# CREATE VECTOR STORE
# ============================================================

def create_vector_store(chunks):

    if not chunks:

        raise ValueError(
            "Cannot create vector store "
            "because chunks are empty."
        )

    print(
        "Creating embeddings..."
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIRECTORY,
        collection_name=COLLECTION_NAME
    )

    print(
        "ChromaDB created successfully."
    )

    return vectorstore


# ============================================================
# CREATE RETRIEVER
# ============================================================

def create_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4
        }
    )

    return retriever


# ============================================================
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful document assistant.

Answer the question using ONLY the context below.

Rules:

1. Do not use outside knowledge.
2. Do not make up information.
3. If the answer is not available in the context,
   say exactly:

"I could not find the answer in the document."

Context:
----------------
{context}
----------------

Question:
{question}

Answer:
"""
)


# ============================================================
# FORMAT DOCUMENTS
# ============================================================

def format_documents(documents):

    if not documents:

        return "No relevant context was found."

    formatted_documents = []

    for document in documents:

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        formatted_documents.append(
            f"[Page {page}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(
        formatted_documents
    )


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(
    retriever,
    question
):

    documents = retriever.invoke(
        question
    )

    context = format_documents(
        documents
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return answer, documents