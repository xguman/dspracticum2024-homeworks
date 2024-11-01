from datasets import Dataset, load_dataset
from huggingface_hub import login
import os

# Specify the directory containing text files
data_dir = 'text_files'
data_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.txt')]

# Prepare data in the desired format
data = []
for file_path in data_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    data.append({"text": content, "file_name": os.path.basename(file_path)})

# Create a Dataset object from the data
dataset = Dataset.from_dict({"text": [item["text"] for item in data], "file_name": [item["file_name"] for item in data]})

# Save the dataset to disk
dataset.save_to_disk('/Users/peterguman/MUNI/M7DataSP/text_dataset/processed_dataset')

# Push dataset to Hugging Face Hub
dataset.push_to_hub("xguman/hw5_text_dataset", private=False)
