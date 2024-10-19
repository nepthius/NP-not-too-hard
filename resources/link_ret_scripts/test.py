import requests
from bs4 import BeautifulSoup
import csv
import time
import re

# Base URL for the search results
base_url = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=ALL_ALL&DB_TYPE_OF_ACT=regulation&DTS_SUBDOM=ALL_ALL&textScope0=ti&typeOfActStatus=REGULATION&DTS_DOM=ALL&lang=en&type=advanced&date0=ALL%3A01012013%7C31012025&qid=1729257462451&andText0=Regulation+%28EU%29"

# Function to scrape a single CELEX page to extract the ELI link and proper regulation name
def scrape_celex_page(celex_link, row_index):
    try:
        print(f"Processing row {row_index}: {celex_link}")
        response = requests.get(celex_link)
        response.raise_for_status()  # Raise exception for bad requests
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the regulation name inside the 'title-bold' class
        reg_name = None
        reg_name_tag = soup.find('p', class_='title-bold')
        if reg_name_tag:
            full_reg_name = reg_name_tag.get_text(strip=True)
            # Use regex to extract only "Regulation (EU) YYYY/####"
            match = re.search(r'Regulation \(EU\) \d{4}/\d+', full_reg_name)
            if match:
                reg_name = match.group(0)
        
        # Find the ELI link in the 'a' tag with specific title
        eli_link = None
        eli_link_tag = soup.find('a', href=True, title="Gives access to this document through its ELI URI.")
        if eli_link_tag:
            eli_link = eli_link_tag['href']

        # Logging for checking if the ELI link or regulation name was not found
        if not eli_link or not reg_name:
            print(f"Row {row_index}: ELI link or regulation name not found.")
        else:
            print(f"Row {row_index}: Found ELI link: {eli_link}, Regulation name: {reg_name}")

        return eli_link, reg_name

    except Exception as e:
        print(f"Error processing CELEX link at row {row_index}: {e}")
        return None, None

# Function to scrape a single page from the search results
def scrape_page(page_num):
    url = f"{base_url}&page={page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    regulations = []

    # Loop through each regulation item on the page
    for i, item in enumerate(soup.find_all('a', id=True, class_='title')):
        celex_link = f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{item['href'].split('CELEX:')[1].split('&')[0]}&qid=1729257462451"
        
        # Scrape the CELEX page for the ELI link and regulation name
        eli_link, reg_name = scrape_celex_page(celex_link, i + 1)

        # If the ELI link and regulation name were successfully scraped, add them to the list
        if eli_link and reg_name:
            regulations.append((reg_name, eli_link, celex_link))

    return regulations

# Function to save the results to CSV
def save_to_csv(regulations, filename='regulations_links_all_pages.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Regulation Name', 'ELI Link', 'CELEX Link'])
        writer.writerows(regulations)

# Main function to loop through all pages and scrape the data
def scrape_all_pages(pages_to_scrape=1):
    all_regulations = []
    for page in range(1, pages_to_scrape + 1):
        print(f"Scraping page {page}...")
        regulations = scrape_page(page)
        print(f"Page {page}: Scraped {len(regulations)} regulations.")
        all_regulations.extend(regulations)
        time.sleep(1)  # Delay between requests to avoid overloading the server

    save_to_csv(all_regulations)

# Run the scraper for the first 150 pages
if __name__ == "__main__":
    scrape_all_pages(pages_to_scrape=1)
