import os
from datasets import load_dataset
from PIL import Image

def download_images(name="food101"):
    dataset = load_dataset(name, split="train[:1%]")  # Get a small percentage of the data

    output_dir = "data/pictures"
    os.makedirs(output_dir, exist_ok=True)

    num_images = 300
    count = 0

    for example in dataset:
        if count >= num_images:
            break
        image = example['image']
        image.save(os.path.join(output_dir, f"image_{count}.jpg"))  # Save as JPG
        count += 1

    print(f"Downloaded and saved {count} images to the folder '{output_dir}'")
