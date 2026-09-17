
import torch
from PIL import Image

from transformers import(
    CLIPProcessor, CLIPModel
)

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

image = Image.open(
    "cat.jpg",
).convert("RGB")

inputs = processor(images=image, return_tensors="pt")

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

image = processor(images = image, return_tensors="pt")

with torch.no_grad():
    image_features = model.get_image_features(**inputs)

image_features = image_features / image_features.norm(
    dim=-1,keepdim=True
)

print("Embedding shape:",image_features.shape)
print("First values:",image_features[0][:10])
