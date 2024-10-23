import os
import requests
from bs4 import BeautifulSoup

os.makedirs('files', exist_ok=True)

url = 'https://www.finos.org/faq'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#pretty basic, all this scrapes is just the question and answer from the html
with open('files/finos.txt', 'w', encoding='utf-8') as f:
    for item in soup.find_all('div', class_='hs-accordion__item'):
        question = item.find('button').get_text(strip=True)
        answer = item.find('div', class_='hs-accordion__item-content').get_text(strip=True)
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n\n")

print("Done :), look here -> 'files/finos.txt'")
