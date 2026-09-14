
import chromadb
import ollama

EMBEDDING_MODEL = "embeddinggemma"

documents = [
    "Java is a popular programming language used for backend development.",
    "Spring Boot is a framework for building Java backend applications.",
    "Python is widely used for artificial intelligence and machine learning.",
    "Chroma is a vector database used for storing and searching embeddings.",
    "Ollama allows developers to run large language models locally.",
    "Docker is a platform used to package applications into containers.",
    "Redis is an in-memory data store commonly used for caching.",
]

def create_embeddings(documents):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=documents,
    )

    return response["embeddings"]

def main():
    # create persistent chroma database

    client = chromadb.PersistentClient(path="./db/chroma_db")
    collection = client.get_or_create_collection(name="ai_learning")

    # generate embeddings
    embeddings = create_embeddings(documents=documents)

    #store documents + vectors
    collection.upsert(
        ids=[str(i) for i in range(len(documents))],
        documents=documents,
        embeddings=embeddings
    )

    print("Documents stored successfully!.")

    print("\n Number of documents:")
    print(collection.count())

if __name__ == "__main__":
    main()    

# Documents stored successfully!.

#  Number of documents:
# 7




