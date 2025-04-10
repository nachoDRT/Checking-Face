import torch
from transformers import AutoTokenizer, AutoModelForZeroShotImageClassification
from PIL import Image
import requests
from torchvision import transforms

import torch
from transformers import AutoTokenizer, AutoModelForZeroShotImageClassification
from PIL import Image
import requests
from torchvision import transforms

def zero_shot_image_classification_siglip(image_urls, texts, ckpt="google/siglip2-so400m-patch14-384", max_length=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Cargar modelo y tokenizer
    model = AutoModelForZeroShotImageClassification.from_pretrained(ckpt).to(device)
    tokenizer = AutoTokenizer.from_pretrained(ckpt)

    preprocess = transforms.Compose([
        transforms.Resize(384, interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.CenterCrop(384),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    # Cargar imágenes
    images = []
    for url in image_urls:
        img = Image.open(requests.get(url, stream=True).raw).convert("RGB")
        images.append(preprocess(img))
    images_tensor = torch.stack(images).to(device)

    # Tokenizar textos
    text_inputs = tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    ).to(device)

    model_inputs = {
        "pixel_values": images_tensor,
        "input_ids": text_inputs["input_ids"]
    }
    if "attention_mask" in text_inputs:
        model_inputs["attention_mask"] = text_inputs["attention_mask"]

    with torch.no_grad():
        outputs = model(**model_inputs)

    # Extraer embeddings
    image_embeds = outputs.image_embeds  # shape: [num_images, dim]
    text_embeds = outputs.text_embeds    # shape: [num_texts, dim]

    # Normalizar para similitud coseno
    image_embeds = torch.nn.functional.normalize(image_embeds, dim=-1)
    text_embeds = torch.nn.functional.normalize(text_embeds, dim=-1)

    # Calcular similitud coseno
    similarity = image_embeds @ text_embeds.T  # shape: [num_images, num_texts]

    results = []
    for image_idx, scores in enumerate(similarity):
        ranked = sorted(zip(texts, scores.tolist()), key=lambda x: x[1], reverse=True)
        results.append({
            "image_index": image_idx,
            "ranking": ranked
        })
    return results

if __name__ == "__main__":
    image_urls = [
        "https://huggingface.co/datasets/merve/coco/resolve/main/val2017/000000000285.jpg",  # oso real
        "https://huggingface.co/datasets/merve/coco/resolve/main/val2017/000000000776.jpg",  # osos de peluche
    ]

    texts = [
        "bear looking into the camera",
        "bear looking away from the camera",
        "a bunch of teddy bears",
        "two teddy bears",
        "three teddy bears",
    ]

    resultados = zero_shot_image_classification_siglip(image_urls, texts)

    for res in resultados:
        print(f"\nImagen {res['image_index']}:")
        for label, score in res["ranking"]:
            print(f"  {label}: {score:.4f}")
