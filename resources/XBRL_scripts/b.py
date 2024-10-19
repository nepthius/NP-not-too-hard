import os
import json
import zipfile
import pandas as pd
import re

# Get the current directory where the .py script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the submissions.zip file
submissions_zip_path = os.path.join(current_directory, 'submissions.zip')

# Define your CIK to Ticker mapping for Dow Jones 30 companies
cik_to_ticker = {
    66740: 'MMM', 4962: 'AXP', 318154: 'AMGN', 320193: 'AAPL', 12927: 'BA',
    18230: 'CAT', 93410: 'CVX', 858877: 'CSCO', 21344: 'KO', 1751788: 'DOW',
    886982: 'GS', 354950: 'HD', 773840: 'HON', 51143: 'IBM', 50863: 'INTC',
    200406: 'JNJ', 19617: 'JPM', 63908: 'MCD', 310158: 'MRK', 789019: 'MSFT',
    320187: 'NKE', 80424: 'PG', 1108524: 'CRM', 86312: 'TRV', 731766: 'UNH',
    732712: 'VZ', 1403161: 'V', 1618921: 'WBA', 104169: 'WMT', 1001039: 'DIS'
}

# List of form types we're interested in
desired_form_types = ['10-K', '10-Q', '8-K']

# Create a list to store extracted information
data_records = []

# Regular expression to extract CIK from filenames like 'CIK00000*****' (padded with zeros)
cik_regex = re.compile(r'CIK0*(\d{1,10})')  # Extract the right-most digits, ignoring leading zeros

# Open the ZIP file for reading
with zipfile.ZipFile(submissions_zip_path, 'r') as zip_ref:
    # Loop through each file in the zip archive
    for filename in zip_ref.namelist():
        if filename.endswith(".json"):
            # Extract the CIK number from the filename using regex
            match = cik_regex.search(filename)
            if match:
                cik = int(match.group(1))  # Extract the CIK as an integer
                if cik in cik_to_ticker:
                    ticker = cik_to_ticker[cik]
                    print(f"Processing file: {filename} for ticker: {ticker}")  # Debugging output
                    # Open and read the JSON file inside the zip
                    with zip_ref.open(filename) as file:
                        try:
                            data = json.load(file)
                            company_name = data.get('name', 'Unknown')

                            # Extract recent filings
                            recent_filings = data.get('filings', {}).get('recent', {})
                            accession_numbers = recent_filings.get('accessionNumber', [])
                            filing_dates = recent_filings.get('filingDate', [])
                            form_types = recent_filings.get('form', [])
                            primary_documents = recent_filings.get('primaryDocument', [])

                            # Iterate through the filings and capture details for 10-K, 10-Q, 8-K forms
                            for i in range(len(filing_dates)):
                                form_type = form_types[i]
                                if form_type in desired_form_types:
                                    data_records.append({
                                        'ticker': ticker,
                                        'company_name': company_name,
                                        'accession_number': accession_numbers[i],
                                        'filing_date': filing_dates[i],
                                        'form_type': form_type,
                                        'primary_document': primary_documents[i]
                                    })

                        except (json.JSONDecodeError, TypeError) as e:
                            print(f"Error processing {filename}: {e}")
                            # Skip problematic files and continue processing

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(data_records)

# Save to CSV or JSON format
output_csv_path = os.path.join(current_directory, 'dow_jones_submission_data.csv')
output_json_path = os.path.join(current_directory, 'dow_jones_submission_data.json')

df.to_csv(output_csv_path, index=False)
df.to_json(output_json_path, orient='records')

print(f"Data extraction completed! {len(df)} records saved to {output_csv_path} and {output_json_path}.")