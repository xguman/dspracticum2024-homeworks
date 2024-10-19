import gradio as gr
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from torch.utils.data import Dataset, DataLoader
import os
import numpy as np
import warnings
from create_image_embeddnigs import create_embeddings
from download_dataset import download_images

warnings.filterwarnings("ignore", category=UserWarning)
os.environ["TOKENIZERS_PARALLELISM"] = "true"  # or "false"

download_images()

# get image embeddings. If file «image_embeddings.npy» exists, just load it, otherwise create it
if os.path.exists("image_embeddings.npy"):
    image_embeddings = np.load("image_embeddings.npy")
else:
    image_dir = "data/pictures"
    batch_size = 32
    device = "cuda" if torch.cuda.is_available() else "cpu"
    image_embeddings = create_embeddings(image_dir, batch_size, device)

image_embeddings = image_embeddings / np.linalg.norm(image_embeddings, axis=1, keepdims=True)

def get_text_embeddings(input_text):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    inputs = processor(text=input_text, return_tensors="pt", padding=True, truncation=True)
    embeddings = model.get_text_features(**inputs)
    vector = embeddings.detach().numpy().ravel()
    return vector / np.linalg.norm(vector)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_similar_images(text_embedding, image_embeddings, top_k=4):
    similarities = np.array([cosine_similarity(text_embedding, image_embedding) for image_embedding in image_embeddings])
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    return top_k_indices

def get_similar_images(input_text):
    text_embedding = get_text_embeddings(input_text)
    top_k_indices = find_similar_images(text_embedding, image_embeddings)
    image_paths = [os.path.join("data/pictures", f) for f in os.listdir("data/pictures") if f.endswith(('.png', '.jpg', '.jpeg'))]
    similar_images = [image_paths[i] for i in top_k_indices]
    return [Image.open(image_path) for image_path in similar_images]


if __name__ == "__main__":
    iface = gr.Interface(fn=get_similar_images, inputs="text", outputs="gallery", title="Find Similar Images")
    iface.launch(share=True)
