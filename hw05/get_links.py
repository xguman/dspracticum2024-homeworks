from bs4 import BeautifulSoup
import requests

response = requests.get("https://zlatyfond.sme.sk/autori")
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href=True)
result_links = {}

for link in links:
    href = link['href']
    if href.startswith('/dielo/') and link.text:
        result_links[href] = link.text

for href, title in result_links.items():
    print(f"https://zlatyfond.sme.sk{href}")
