from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from sentence_transformers.util import cos_sim


documents = [
    "Spring Boot is a Java framework for backend development.",
    "Python is useful for machine learning.",
    "Spring Framework provides dependency injection.",
    "Docker containers package applications.",
    "Spring Boot provides auto configuration.",
    "Java is widely used for enterprise software."
]


query = "How does Spring Boot help Java backend development?"


# STEP 1
# Bi-Encoder retrieval

bi_encoder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


doc_embeddings = bi_encoder.encode(
    documents,
    convert_to_tensor=True
)

query_embedding = bi_encoder.encode(
    query,
    convert_to_tensor=True
)


scores = cos_sim(
    query_embedding,
    doc_embeddings
)[0]


top_indices = scores.argsort(
    descending=True
)[:4]


candidates = [
    documents[i]
    for i in top_indices
]


print("Candidates:")

for doc in candidates:
    print(doc)


# STEP 2
# Cross-Encoder reranking

cross_encoder = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


pairs = [
    [query, document]
    for document in candidates
]


rerank_scores = cross_encoder.predict(
    pairs
)


results = list(
    zip(candidates, rerank_scores)
)


results.sort(
    key=lambda x: x[1],
    reverse=True
)


print("\nFinal ranking:")

for document, score in results:

    print(
        f"{score:.4f} → {document}"
    )


# Loading weights: 100%|██████████████████████| 103/103 [00:00<00:00, 3123.38it/s]
# Candidates:
# Spring Boot is a Java framework for backend development.
# Spring Boot provides auto configuration.
# Spring Framework provides dependency injection.
# Java is widely used for enterprise software.
# Loading weights: 100%|██████████████████████| 105/105 [00:00<00:00, 2181.08it/s]

# Final ranking:
# 7.3372 → Spring Boot is a Java framework for backend development.
# 0.3482 → Spring Boot provides auto configuration.
# -4.8390 → Spring Framework provides dependency injection.
# -8.8329 → Java is widely used for enterprise software.