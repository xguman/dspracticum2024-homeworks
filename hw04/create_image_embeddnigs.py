import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from torch.utils.data import Dataset, DataLoader
import os
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class ImageDataset(Dataset):
    def __init__(self, image_dir, processor):
        self.image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.processor = processor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx])
        return self.processor(images=image, return_tensors="pt")['pixel_values'][0]

def get_clip_embeddings_batch(image_dir, batch_size=32, device='cuda'):
    # Load the CLIP model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # Create dataset and dataloader
    dataset = ImageDataset(image_dir, processor)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    all_embeddings = []

    model.eval()
    with torch.no_grad():
        for batch in dataloader:
            batch = batch.to(device)
            embeddings = model.get_image_features(pixel_values=batch)
            all_embeddings.append(embeddings.cpu().numpy())

    return np.concatenate(all_embeddings)

def create_embeddings(image_dir, batch_size, device):
    embeddings = get_clip_embeddings_batch(image_dir, batch_size, device)
    np.save("image_embeddings.npy", embeddings)
    return embeddings