import torch

from PIL import Image

from transformers import (
    CLIPProcessor,
    CLIPModel
)


model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)


image_paths = [
    "cat.jpg",
    "dog.jpg",
    "car.jpg"
]


query = "a photograph of a dog"


# Create text embedding

inputs = processor(
    text=[query],
    return_tensors="pt",
    padding=True
)


with torch.no_grad():

    text_features = model.get_text_features(
        **inputs
    )


text_features = text_features / text_features.norm(
    dim=-1,
    keepdim=True
)


results = []


for path in image_paths:

    image = Image.open(path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        image_features = model.get_image_features(
            **inputs
        )

    image_features = image_features / image_features.norm(
        dim=-1,
        keepdim=True
    )


    similarity = (
        text_features @ image_features.T
    ).item()


    results.append(
        (path, similarity)
    )


results.sort(
    key=lambda x: x[1],
    reverse=True
)


for path, score in results:

    print(
        f"{score:.4f} → {path}"
    )