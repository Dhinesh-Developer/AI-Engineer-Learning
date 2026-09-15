import chromadb
import ollama
from pypdf import PdfReader
import hashlib


EMBEDDING_MODEL = "embeddinggemma"
LLM_MODEL = "qwen2.5:3b"


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="course_notes"
)


def extract_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text:

            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


def chunk_text(
    text,
    chunk_size=800,
    overlap=150
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size - overlap

    return chunks


def add_document(
    pdf_file,
    filename
):

    pages = extract_pdf(pdf_file)

    all_chunks = []
    metadatas = []

    for page in pages:

        chunks = chunk_text(
            page["text"]
        )

        for chunk in chunks:

            all_chunks.append(chunk)

            metadatas.append({
                "source": filename,
                "page": page["page"]
            })


    if not all_chunks:
        return 0


    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=all_chunks
    )

    embeddings = response["embeddings"]


    ids = []

    for index, chunk in enumerate(
        all_chunks
    ):

        raw_id = (
            filename
            + str(index)
            + chunk
        )

        ids.append(
            hashlib.md5(
                raw_id.encode()
            ).hexdigest()
        )


    collection.upsert(
        ids=ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


    return len(all_chunks)


def retrieve(
    question,
    top_k=5
):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    query_embedding = response[
        "embeddings"
    ][0]


    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )


    return results


def generate_answer(
    question,
    results
):

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]


    context_parts = []


    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"""
SOURCE: {metadata['source']}
PAGE: {metadata['page']}

CONTENT:
{document}
"""
        )


    context = "\n\n".join(
        context_parts
    )


    prompt = f"""
You are a course notes assistant.

Answer ONLY using the provided context.

Always mention the source document
when possible.

If the answer is unavailable,
say that you could not find it.

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
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response[
        "message"
    ]["content"]