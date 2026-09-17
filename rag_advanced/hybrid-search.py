from rank_bm25 import BM25Okapi

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


documents = [
    "Spring Security supports JWT authentication.",
    "JWT tokens are commonly used for stateless authentication.",
    "Spring Boot applications can implement role based authorization.",
    "Redis can be used for caching.",
    "Kafka supports event driven architecture."
]


query = "JWT authentication Spring Security"


# -------------------------
# BM25
# -------------------------

tokenized_docs = [
    doc.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized_docs)

bm25_scores = bm25.get_scores(
    query.lower().split()
)


# -------------------------
# Vector Search
# -------------------------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

doc_embeddings = model.encode(
    documents,
    convert_to_tensor=True
)

query_embedding = model.encode(
    query,
    convert_to_tensor=True
)

vector_scores = cos_sim(
    query_embedding,
    doc_embeddings
)[0].cpu().numpy()


# -------------------------
# Normalize scores
# -------------------------

def normalize(scores):

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:
        return [0] * len(scores)

    return [
        (x - minimum) /
        (maximum - minimum)
        for x in scores
    ]


bm25_norm = normalize(
    bm25_scores
)

vector_norm = normalize(
    vector_scores
)


# -------------------------
# Combine
# -------------------------

final_scores = []

for i in range(len(documents)):

    score = (
        0.5 * bm25_norm[i]
        +
        0.5 * vector_norm[i]
    )

    final_scores.append(score)


results = sorted(
    zip(documents, final_scores),
    key=lambda x: x[1],
    reverse=True
)


for document, score in results:

    print(
        f"{score:.4f} → {document}"
    )

# Loading weights: 100%|██████████████████████| 103/103 [00:00<00:00, 6828.31it/s]
# 1.0000 → Spring Security supports JWT authentication.
# 0.4048 → Spring Boot applications can implement role based authorization.
# 0.4048 → JWT tokens are commonly used for stateless authentication.
# 0.0007 → Redis can be used for caching.
# 0.0000 → Kafka supports event driven architecture.    