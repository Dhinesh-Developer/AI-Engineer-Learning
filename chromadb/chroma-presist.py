
import chromadb

from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()

croma_client = chromadb.PersistentClient(path="./db/chroma_presist")

collection = croma_client.get_or_create_collection("my_story",embedding_function=default_ef)

documents = [
    {"id":"doc1", "text":"Hello, World!"},
    {"id":"doc2", "text":"How are you today?"},
    {"id":"doc3", "text":"Goodbye, see you later!"},
    {"id":"doc4", "text":"Microsoft is a technology company that develops software."}
]


for doc in documents:
    collection.upsert(ids=doc["id"], documents=[doc["text"]])

# define a query text
query_text = "Age of the Earth"

result = collection.query(
    query_texts=[query_text],
    n_results=2,
)

for idx, documents in enumerate(result['documents'][0]):
    doc_id = result['ids'][0][idx]
    distance = result['distances'][0][idx]
    print(
        f" For the query: {query_text}, \n Found similar document: {documents} (ID: {doc_id}, Distance: {distance})"
    )




