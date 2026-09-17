
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

documents = [
    "Python is a popular programming language.",
    "Java is commonly used for enterprise applications.",
    "Machine Learning uses algorithms to learn from data.",
    "You can learn python through online courses."
]

query = "How can i study python?"

document_embeddings = model.encode(
    documents,
    convert_to_tensor=True
)

query_embeddings = model.encode(
    documents,
    convert_to_tensor=True
)

scores = cos_sim(
    query_embeddings,
    document_embeddings
)[0]

for document, score in zip(documents, scores):
    print(
        f"{score.item():.4f} -> {document}"
    )

# config.json: 100%|██████████████| 612/612 [00:00<00:00, 1.37MB/s]
# model.safetensors: downloading bytes: ███████| 85.0MB, 3.44MB/s  
# model.safetensors: reconstructing file: 100%|█| 90.9MB / 90.9MB, 
# Loading weights: 100%|██████████████████████| 103/103 [00:00<00:00, 1973.65it/s]
# tokenizer_config.json: 100%|███████████████████| 350/350 [00:00<00:00, 1.57MB/s]
# vocab.txt: 100%|█████████████████████████████| 232k/232k [00:00<00:00, 2.63MB/s]
# tokenizer.json: 100%|████████████████████████| 466k/466k [00:00<00:00, 5.66MB/s]
# special_tokens_map.json: 100%|██████████████████| 112/112 [00:00<00:00, 320kB/s]
# config.json: 100%|██████████████████████████████| 190/190 [00:00<00:00, 417kB/s]
# 1.0000 -> Python is a popular programming language.
# 0.4244 -> Java is commonly used for enterprise applications.
# 0.2169 -> Machine Learning uses algorithms to learn from data.
# 0.6320 -> You can learn python through online courses.