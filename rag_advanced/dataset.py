from datasets import load_dataset
from datasets import load_from_disk

dataset = load_dataset(
    "cornell-movie-review-data/rotten_tomatoes",
    split="train"
)

print(dataset)
print(dataset[0])

# README.md: 100%|████████████| 7.46k/7.46k [00:00<00:00, 10.2MB/s]
# train.parquet: downloading bytes: ███████████|  697kB, 62.8kB/s  
# train.parquet: reconstructing file: 100%|█|  699kB /  699kB, 64.1
# validation.parquet: downloading bytes: ██████| 88.9kB, 8.37kB/s  
# validation.parquet: reconstructing file: 100%|█| 90.0kB / 90.0kB,
# test.parquet: downloading bytes: ████████████| 91.4kB, 8.64kB/s  
# test.parquet: reconstructing file: 100%|█| 92.2kB / 92.2kB, 8.73k
# Generating train split: 100%|█| 8530/8530 [00:00<00:00, 209923.15
# Generating validation split: 100%|█| 1066/1066 [00:00<00:00, 2048
# Generating test split: 100%|█| 1066/1066 [00:00<00:00, 188036.34 
# Dataset({
#     features: ['text', 'label'],
#     num_rows: 8530
# })
# {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}

print(dataset.column_names)

for item in dataset.select(range(5)):
    print(item)

dataset = load_from_disk(
    "./movie_dataset"
)    
print(dataset[0])
