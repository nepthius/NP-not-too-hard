import json
import csv

def parse_text_file(file_path):
    terms = []
    definitions = []
    current_term = None
    current_definition = []

    #basically just grab the terms/defs and save them
    with open(file_path, 'r') as file:
        for x in file:
            x = x.strip()
            if x == "":
                continue
            if not x[0].isspace() and x.isalpha():
                if current_term and current_definition:
                    terms.append(current_term)
                    definitions.append(" ".join(current_definition).strip())
                current_term = x
                current_definition = []
            else:
                current_definition.append(x)
        if current_term and current_definition:
            terms.append(current_term)
            definitions.append(" ".join(current_definition).strip())

    return terms, definitions


def writer_stuff(terms, definitions, output_file):
    with open(output_file, 'w', newx='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Term', 'Definition'])
        for term, definition in zip(terms, definitions):
            writer.writerow([term, definition])

file_path = 'terms_and_definitions.txt'
csv_output = 'terms_and_definitions.csv'
json_output = 'terms_and_definitions.json'
terms, definitions = parse_text_file(file_path)
writer_stuff(terms, definitions, csv_output)