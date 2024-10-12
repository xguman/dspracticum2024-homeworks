import gradio as gr
import pickle as pkl

import timm
from fastai.vision.all import *
from pathlib import Path

learn = load_learner('model.pkl')

categories = learn.dls.vocab

# Function to classify an image
def classify_image(img):
    pred, idx, probs = learn.predict(img)
    return dict(zip(categories, map(float, probs)))  # Map categories to their probabilities

# Define Gradio input and output components using the updated API
image = gr.Image(width=224, height=224)  # Image input with fixed shape
label = gr.Label()  # Output label to display classification
examples = ['test_image1', 'test_image2']  # Path to image(s) for demonstration

# Create and launch the Gradio interface
intf = gr.Interface(fn=classify_image, inputs=image, outputs=label, examples=examples)
intf.launch(share=True)