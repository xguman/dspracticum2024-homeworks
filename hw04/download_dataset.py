import os
from datasets import load_dataset
from PIL import Image
import random

def download_images(name="food101"):
    dataset = load_dataset(name, split="train")

    # Create a directory to save the images if it doesn't exist
    output_dir = "data/pictures"
    os.makedirs(output_dir, exist_ok=True)

    # Limit to 500 images
    num_images = 500
    
    # Randomly select and save the images
    random_indices = random.sample(range(len(dataset)), num_images)
    for index in random_indices:
        example = dataset[index]
        image = example['image']
        image.save(os.path.join(output_dir, f"image_{count}.jpg"))  # Save as JPG

    print(f"Downloaded and saved {num_images} images to the folder '{output_dir}'")
