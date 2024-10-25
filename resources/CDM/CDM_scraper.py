import os
import requests
from bs4 import BeautifulSoup

# Set up the base URL and output directory
BASE_URL = 'https://cdm.finos.org'
HOME_URL = BASE_URL + '/docs/home'
OUTPUT_DIR = 'cdm_docs'

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_soup(url):
    """Get BeautifulSoup object from the given URL"""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to access {url}")
        return None

def scrape_page(url, file_name):
    """Scrape content from a page and save it to a .txt file"""
    soup = get_soup(url)
    if soup:
        # Find the main content area, typically inside article tags
        content = soup.find('article')
        if content:
            # Extract text and save it to a file
            with open(os.path.join(OUTPUT_DIR, file_name), 'w', encoding='utf-8') as file:
                file.write(content.get_text(separator='\n').strip())
            print(f"Saved content from {url} to {file_name}")
        else:
            print(f"Content not found in {url}")

def main():
    # Scrape the homepage to find all links to documentation pages
    homepage_soup = get_soup(HOME_URL)
    
    if homepage_soup:
        # Find the sidebar navigation which contains the links
        sidebar = homepage_soup.find('nav', {'aria-label': 'Docs sidebar'})
        
        # Iterate through the links in the sidebar
        for link in sidebar.find_all('a', href=True):
            link_text = link.get_text().strip()
            link_href = link['href']

            # Some links might be relative, so make them absolute
            if not link_href.startswith('http'):
                link_href = BASE_URL + link_href

            # Create a valid file name by replacing spaces with underscores and adding '.txt'
            file_name = link_text.replace(' ', '_') + '.txt'

            # Scrape each page and save its content
            scrape_page(link_href, file_name)

if __name__ == "__main__":
    main()
