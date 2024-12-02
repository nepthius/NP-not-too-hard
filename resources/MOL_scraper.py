import requests
from bs4 import BeautifulSoup
import os


base_url = "https://opensource.org/licenses"
page_url_base = "https://opensource.org/licenses/page/"

# scrape for each license in MOL
def scrape_license_page(url, license_name):
    print(f"Scraping license page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    license_info = soup.find('div', {'class': 'entry-content post--content license-content'})
    
    if license_info:

        license_text = license_info.get_text(separator='\n').strip()


        filename = f"MOF/{license_name}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(license_text)
        print(f"Saved {license_name} license to {filename}")
    else:
        print(f"Could not find information for {license_name}")

def scrape_license_list(page_number):
    if page_number == 1:
        url = base_url
    else:
        url = f"{page_url_base}{page_number}"

    print(f"Scraping page URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    license_rows = soup.find_all('tr')

    for row in license_rows:
        link = row.find('a', href=True)
        if link:
            license_name = link['href'].split('/')[-1]
            license_url = f"{link['href']}"
            scrape_license_page(license_url, license_name)

for page in range(1, 12):
    print(f"Scraping page {page}...")
    scrape_license_list(page)

print("Scraping completed!")
