from datasets import load_dataset
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

dataset = load_dataset(
    "cornell-movie-review-data/rotten_tomatoes",
    split="train"
)

texts = []

for item in dataset.select(range(100)):
    text = item["text"]
    texts.append(text)

embeddings = OllamaEmbeddings(
    model="embeddinggemma"
)

vectorstore = Chroma.from_texts(
    texts,embedding=embeddings,
    persist_directory="./movie_chroma",
    collection_name="movie_reviews"
)

query = "A movie that is very entertaining"

results = vectorstore.similarity_search(query=query,k=5)

for res in results:
    print(res.page_content)


