
import chromadb
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()
chroma_client = chromadb.Client()

collection_name = "test_collection"

collection = chroma_client.get_or_create_collection(collection_name, embedding_function=default_ef)

# Define a text documents

documents = [
    {"id":"doc1", "text":"Hello, World!"},
    {"id":"doc2", "text":"How are you today!"},
    {"id":"doc3", "text":"Goodbye, see you later!"},
]

for doc in documents:
    collection.upsert(ids=doc["id"], documents=[doc["text"]])

# define q query text
query_text = "Hello, World!"

result = collection.query(
    query_texts= [query_text],
    n_results=3,
)

# print(result)

for idx, documents in enumerate(result['documents'][0]):
    doc_id = result['ids'][0][idx]
    distance = result['distances'][0][idx]
    print(
        f" For the query: {query_text}, \n Found similar document: {documents} (ID: {doc_id}, Distance: {distance})"
    )

# res
#100%|██████████████████████████████| 79.3M/79.3M [00:20<00:00, 4.06MiB/s]
#{'ids': [['doc1', 'doc2', 'doc3']], 'embeddings': None, 'documents': [['Hello, World!', 'How are you today!', 'Goodbye, see you later!']], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[None, None, None]], 'distances': [[0.0, 1.1371561288833618, 1.1922802925109863]]}


#  For the query: Hello, World!, 
#  Found similar document: Hello, World! (ID: doc1, Distance: 0.0)
#  For the query: Hello, World!, 
#  Found similar document: How are you today! (ID: doc2, Distance: 1.1371561288833618)
#  For the query: Hello, World!, 
#  Found similar document: Goodbye, see you later! (ID: doc3, Distance: 1.1922802925109863)