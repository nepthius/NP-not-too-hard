import zipfile
import json
import csv

# Path to your companyfacts.zip and output CSV file
zip_file_path = "companyfacts.zip"
output_csv_path = "dow_jones_labels.csv"

# CIK to Ticker mapping for Dow Jones 30 index companies
cik_to_ticker = {
    66740: 'MMM', 4962: 'AXP', 318154: 'AMGN', 320193: 'AAPL', 12927: 'BA',
    18230: 'CAT', 93410: 'CVX', 858877: 'CSCO', 21344: 'KO', 1751788: 'DOW',
    886982: 'GS', 354950: 'HD', 773840: 'HON', 51143: 'IBM', 50863: 'INTC',
    200406: 'JNJ', 19617: 'JPM', 63908: 'MCD', 310158: 'MRK', 789019: 'MSFT',
    320187: 'NKE', 80424: 'PG', 1108524: 'CRM', 86312: 'TRV', 731766: 'UNH',
    732712: 'VZ', 1403161: 'V', 1618921: 'WBA', 104169: 'WMT', 1001039: 'DIS'
}

# Convert CIK keys to strings since they may appear as strings in JSON
cik_to_ticker = {str(k): v for k, v in cik_to_ticker.items()}

# Step 1: Open the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # List all files in the zip
    file_list = zip_ref.namelist()

    # Filter JSON files corresponding to Dow Jones companies based on CIK
    json_files = [f for f in file_list if any(cik in f for cik in cik_to_ticker.keys())]

    # Step 2: Create a set to store unique labels
    all_labels = set()

    # Step 3: For each JSON file, read and extract labels from "facts"
    for json_file in json_files:
        with zip_ref.open(json_file) as file:
            try:
                # Load the JSON content
                data = json.load(file)

                # Check if "facts" key exists
                if "facts" in data:
                    facts = data["facts"]
                    
                    # Loop through the facts and gather all unique labels
                    for key in facts.keys():
                        sub_labels = facts[key].keys()
                        all_labels.update(sub_labels)
                    
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {json_file}")

# Step 4: Write the unique labels to a CSV file
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Unique Labels"])
    
    for label in sorted(all_labels):
        writer.writerow([label])

print(f"Unique labels have been saved to {output_csv_path}")
