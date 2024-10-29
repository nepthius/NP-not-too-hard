import os
import requests
from bs4 import BeautifulSoup

#create some basic links and just grab cdm resources
BASE_URL = 'https://cdm.finos.org'
HOME_URL = BASE_URL + '/docs/home'
OUTPUT_DIR = 'cdm_docs'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_soup(url):
    """beuatiful soup object"""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to access :((((( {url}")
        return None

def scrape_page(url, file_name):
    soup = get_soup(url)
    if soup:
        content = soup.find('article')
        if content:
            with open(os.path.join(OUTPUT_DIR, file_name), 'w', encoding='utf-8') as file:
                file.write(content.get_text(separator='\n').strip())
            print(f"GOT IT!! {url} to {file_name}")
        else:
            print(f"ruh roh {url}")

def main():
    homepage_soup = get_soup(HOME_URL)
    if homepage_soup:
        sidebar = homepage_soup.find('nav', {'aria-label': 'Docs sidebar'})
        for link in sidebar.find_all('a', href=True):
            link_text = link.get_text().strip()
            link_href = link['href']
            if not link_href.startswith('http'):
                link_href = BASE_URL + link_href
            file_name = link_text.replace(' ', '_') + '.txt'
            scrape_page(link_href, file_name)

if __name__ == "__main__":
    main()
