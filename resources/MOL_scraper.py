import requests
from bs4 import BeautifulSoup
import os

# Base URL for the licenses listing and license pages
base_url = "https://opensource.org/licenses"
page_url_base = "https://opensource.org/licenses/page/"

# Function to scrape license details from an individual license page
def scrape_license_page(url, license_name):
    print(f"Scraping license page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the main body of the license content
    license_info = soup.find('div', {'class': 'entry-content post--content license-content'})
    
    if license_info:
        # Extract the text, preserving line breaks
        license_text = license_info.get_text(separator='\n').strip()

        # Save the license text to a file named after the license
        filename = f"MOF/{license_name}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(license_text)
        print(f"Saved {license_name} license to {filename}")
    else:
        print(f"Could not find information for {license_name}")

# Function to scrape each page of licenses, following links to individual licenses
def scrape_license_list(page_number):
    if page_number == 1:
        url = base_url
    else:
        url = f"{page_url_base}{page_number}"

    print(f"Scraping page URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links to individual licenses on the page
    license_rows = soup.find_all('tr')

    for row in license_rows:
        link = row.find('a', href=True)
        if link:
            license_name = link['href'].split('/')[-1]
            license_url = f"{link['href']}"
            scrape_license_page(license_url, license_name)

# Loop over all 11 pages of the license list
for page in range(1, 12):
    print(f"Scraping page {page}...")
    scrape_license_list(page)

print("Scraping completed!")
