import csv
def parse(file_path):
    acronyms = []
    definitions = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if "__________" in line: #i'll change this curation line later (just keeping for manual parse issues)
                acronym, definition = line.split("__________", 1)
                acronyms.append(acronym.strip())
                definitions.append(definition.strip())
    return acronyms, definitions
def writer_stuff(acronyms, definitions, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Acronym', 'Definition'])
        for acronym, definition in zip(acronyms, definitions):
            writer.writerow([acronym, definition])
file_path = '../../gen-texts/SBOA.txt'
csv_output = '../../training-sets/definitions/SBOA.csv'
acronyms, definitions = parse(file_path)
writer_stuff(acronyms, definitions, csv_output)
