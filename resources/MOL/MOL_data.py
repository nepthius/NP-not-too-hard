import os
import csv
import re

def extract_license_name(text):
    lines = text.split('\n')
    license_name = None
    for line in lines[:10]: 
        line = line.strip()
        if not line:
            continue
        match = re.search(r'Licence\s+(.*)', line, re.IGNORECASE)
        if match:
            license_name = match.group(1).strip()
            break
        elif 'licence' in line.lower() or 'license' in line.lower():
            license_name = line.strip()
            break
    if not license_name:
        license_name = 'Unknown License'
    return license_name

def process_files(input_directory, output_csv):
    """
    Process all MOL Licenses.txt
    """
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'License Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in os.listdir(input_directory):
            if filename.lower().endswith('.txt'):
                filepath = os.path.join(input_directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    license_name = extract_license_name(text)
                    writer.writerow({'File Name': filename, 'License Name': license_name})
                    print(f"Processed {filename}: {license_name}")

if __name__ == "__main__":
    input_directory = './MOL' 
    output_csv = 'licenses_output.csv'
    process_files(input_directory, output_csv)
    print(f"License names have been extracted to {output_csv}.")
