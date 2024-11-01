import requests
from bs4 import BeautifulSoup, Comment
import os

# Directory containing the HTML files
html_folder = '/Users/peterguman/MUNI/M7DataSP/text_dataset/downloaded_html'

def extract_text(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <div> with id="stred"
    stred_div = soup.find('div', id='stred')

    # Find the comment <!-- text kapitoly -->
    comments = stred_div.find_all(string=lambda text: isinstance(text, Comment))
    text_kapitoly_comment = None
    for comment in comments:
        if 'text kapitoly' in comment:
            text_kapitoly_comment = comment
            break

    # Extract the text directly under the comment
    if text_kapitoly_comment:
        text_kapitoly_section = text_kapitoly_comment.find_next_sibling('p').get_text(strip=True)
        return text_kapitoly_section
    else:
        print("Comment <!-- text kapitoly --> not found.")


# Iterate over each file in the directory
for filename in os.listdir(html_folder):
    if filename.endswith('.html'):
        file_path = os.path.join(html_folder, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                text = extract_text(html_content)
                
                basename = os.path.basename(filename)
                if text:
                        with open('/Users/peterguman/MUNI/M7DataSP/text_dataset/text_files/{}.txt'.format(basename), 'w', encoding='utf-8') as text_file:
                            text_file.write(text)
        except Exception as e:
            print("Error processing file:", e)