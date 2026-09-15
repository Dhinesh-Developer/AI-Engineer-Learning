import chromadb
import ollama
from pypdf import PdfReader
import hashlib

EMBEDDING_MODEL = "embeddinggemma"
LLM_MODEL = "llama3.2"

# chromaDB

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name = "pdf_documents"
)

# pdf text extraction

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text +"\n"
    return text

# chunking

def chunk_text(text, chunk_size=800,overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start+chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Embeddings

def create_embeddings(texts):

    response = ollama.embed(
        model = EMBEDDING_MODEL,
        input= texts
    )            
    return response["embeddings"]


# Add pdf

def add_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)

    if not text.strip():
        return 0

    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    ids = []

    for chunk in chunks:
        doc_id = hashlib.md5(chunk.encode()).hexdigest()

        ids.append(doc_id)

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )    

    return len(chunks)

# retrival

def retrieve(question, top_k=3):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    query_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return {
        "documents": results["documents"][0],
        "ids": results["ids"][0],
        "distances": results["distances"][0]
    }

# Generate answer

def generate_answer(
        question,
        retrieved_documents
):

    context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are a helpful assistant.
Answer the question ONLY using the context below.
If the answer cannot be found in the context:
say:
"I could not find this information in the document."
Do not invent information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:

"""
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response["message"]["content"]

