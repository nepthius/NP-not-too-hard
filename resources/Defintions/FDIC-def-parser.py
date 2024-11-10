import csv

def parse_acronym_file(file_path):
    acronyms = []
    definitions = []
    #going over each def and term and then appending to their list
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if "-" in line:
                acronym, definition = line.split(" - ", 1)
                acronyms.append(acronym.strip())
                definitions.append(definition.strip())
    return acronyms, definitions
def writer_stuff(acronyms, definitions, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Acronym', 'Definition'])
        for acronym, definition in zip(acronyms, definitions):
            writer.writerow([acronym, definition])
file_path = '../../gen-texts/FDIC.txt'
csv_output = '../../gen-texts/acronyms_and_definitions.csv'
acronyms, definitions = parse_acronym_file(file_path)
writer_stuff(acronyms, definitions, csv_output)
