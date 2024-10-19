import requests
from bs4 import BeautifulSoup
import csv
import re

# Function to scrape the ELI link and correct regulation name from the CELEX page
def scrape_eli_and_name(celex_link, row_index):
    try:
        print(f"Processing row {row_index}: {celex_link}")
        
        response = requests.get(celex_link)
        response.raise_for_status()  # Raise exception for bad requests
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Attempting to extract the ELI link from the 'a' tag with a known title
        eli_element = soup.find('a', href=True, title="Gives access to this document through its ELI URI.")
        eli_link = eli_element['href'] if eli_element else None
        
        # Extracting the regulation name from the page's content
        reg_name = None
        reg_name_element = soup.find('div', class_='PP1Contents')  # Adjust this to the correct div
        if reg_name_element:
            reg_name_text = reg_name_element.get_text(strip=True)
            # Regex to extract the correct format: Regulation (EU) year/number
            match = re.search(r'Regulation \(EU\) \d{4}/\d+', reg_name_text)
            if match:
                reg_name = match.group(0)

        # Handle case where neither ELI nor regulation name were found
        if not eli_link or not reg_name:
            print(f"Row {row_index} processed, but no ELI link or regulation name was found.")
        else:
            print(f"Row {row_index} processed. ELI link: {eli_link}, Regulation name: {reg_name}")

        return eli_link, reg_name

    except Exception as e:
        print(f"Error scraping row {row_index} ({celex_link}): {e}")
        return None, None

# Function to process the CSV and update the ELI links and regulation names
def process_celex_links(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Process each row to visit the CELEX link and scrape the details
    for i, row in enumerate(rows[1:], start=2):  # Skip the header row
        celex_link = row[2]  # CELEX link is the third column
        full_celex_link = celex_link if celex_link.startswith('https') else f"https://eur-lex.europa.eu{celex_link}"
        
        # Scrape the ELI link and regulation name
        eli_link, reg_name = scrape_eli_and_name(full_celex_link, i)

        if eli_link and reg_name:
            rows[i - 1][1] = eli_link  # Update ELI link in the second column
            rows[i - 1][0] = reg_name  # Update the regulation name in the first column

    # Write the updated data back to a new CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Main
if __name__ == "__main__":
    input_csv = 'regulation_links.csv'  # Input CSV with incorrect names and missing ELI links
    output_csv = 'corrected_regulations.csv'  # Output CSV with corrected data
    process_celex_links(input_csv, output_csv)
    print(f"Processed CELEX links and saved corrected data to {output_csv}")
