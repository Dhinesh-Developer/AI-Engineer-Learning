import ollama

MODEL = "embeddinggemma"

texts = [
    "Java is a programming language.",
    "Pythong is widely used for artifical intelligence.",
    "Spring boot is a java backend framework"
]

def generate_embeddings(texts):
    response = ollama.embed(
        model=MODEL,
        input=texts
    )

    return response

def main():
    embeddings = generate_embeddings(texts=texts)

    for text,vector in zip(texts, embeddings):
        print("\nText:",text)
        print("\nVector dimension:",len(vector))
        print("\nFirst 10 values: ")
        print(vector[:10])
        print("-"*10)

if __name__ == "__main__":
    main()        




