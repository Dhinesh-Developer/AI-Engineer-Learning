from sentence_transformers import CrossEncoder


model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


query = "What is Spring Boot?"


documents = [
    "Spring Boot is a Java framework for building backend applications.",
    "Python is used for machine learning.",
    "Spring Boot simplifies configuration of Spring applications.",
    "Docker is a containerization platform."
]


pairs = [
    [query, document]
    for document in documents
]


scores = model.predict(pairs)


for document, score in zip(documents, scores):

    print(
        f"{score:.4f} → {document}"
    )

# model.safetensors: downloading bytes: ██████████████████████| 86.0MB,  272kB/s  
# model.safetensors: reconstructing file: 100%|██████| 90.9MB / 90.9MB, 2.28MB/s  
# Loading weights: 100%|██████████████████████| 105/105 [00:00<00:00, 4381.67it/s]
# tokenizer_config.json: 100%|███████████████| 1.33k/1.33k [00:00<00:00, 2.52MB/s]
# vocab.txt: 100%|█████████████████████████████| 232k/232k [00:00<00:00, 1.80MB/s]
# tokenizer.json: 100%|████████████████████████| 711k/711k [00:00<00:00, 6.41MB/s]
# special_tokens_map.json: 100%|██████████████████| 132/132 [00:00<00:00, 217kB/s]
# 10.6052 → Spring Boot is a Java framework for building backend applications.
# -11.1411 → Python is used for machine learning.
# 7.1227 → Spring Boot simplifies configuration of Spring applications.
# -10.4829 → Docker is a containerization platform.