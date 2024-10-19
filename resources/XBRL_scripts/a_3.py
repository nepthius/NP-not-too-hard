import os
import zipfile
import json

# Dow Jones 30 index CIKs
dow_jones_cik = {
    66740: 'MMM', 4962: 'AXP', 318154: 'AMGN', 320193: 'AAPL', 12927: 'BA',
    18230: 'CAT', 93410: 'CVX', 858877: 'CSCO', 21344: 'KO', 1751788: 'DOW',
    886982: 'GS', 354950: 'HD', 773840: 'HON', 51143: 'IBM', 50863: 'INTC',
    200406: 'JNJ', 19617: 'JPM', 63908: 'MCD', 310158: 'MRK', 789019: 'MSFT',
    320187: 'NKE', 80424: 'PG', 1108524: 'CRM', 86312: 'TRV', 731766: 'UNH',
    732712: 'VZ', 1403161: 'V', 1618921: 'WBA', 104169: 'WMT', 1001039: 'DIS'
}

# Paths
zip_file_path = 'companyfacts.zip'  # Update with the correct path to your .zip file
output_dir = './dow_jones_sample'  # Directory to save extracted files

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Extract one file for each Dow Jones company
with zipfile.ZipFile(zip_file_path, 'r') as z:
    for cik in dow_jones_cik:
        found_file = False
        for filename in z.namelist():
            if str(cik) in filename and filename.endswith('.json'):
                print(f"Extracting {filename} for {dow_jones_cik[cik]}")
                z.extract(filename, output_dir)
                found_file = True
                break  # Stop after finding the first file for this CIK
        if not found_file:
            print(f"No file found for CIK {cik} ({dow_jones_cik[cik]})")

print("Extraction complete. Files saved in:", output_dir)
