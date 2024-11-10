import json
import csv

def parsing(file_path):
    terms = []
    definitions = []
    #basically going over each def and term and then appending to their respective list
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        for i in range(0, len(lines), 2):
            term = lines[i]
            definition = lines[i + 1] if i + 1 < len(lines) else ""
            terms.append(term)
            definitions.append(definition)
    return terms, definitions
def writer_stuff(terms, definitions, output_file):
    #writing term def into usable training format
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Term', 'Definition'])
        for term, definition in zip(terms, definitions):
            writer.writerow([term, definition])

file_path = 'acronyms_and_definitions.txt'
csv_output = 'acronyms_and_definitions.csv'
json_output = 'acronyms_and_definitions.json'
terms, definitions = parsing(file_path)
writer_stuff(terms, definitions, csv_output)
