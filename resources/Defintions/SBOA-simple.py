import csv
def parse(file_path):
    acronyms = []
    definitions = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ": " in line:  #simple split here
                acronym, definition = line.split(": ", 1)
                acronyms.append(acronym.strip())
                definitions.append(definition.strip())
    return acronyms, definitions
def writer_stuff(acronyms, definitions, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Acronym', 'Definition'])
        for acronym, definition in zip(acronyms, definitions):
            writer.writerow([acronym, definition])
file_path = '../../gen-texts/sboa-simple.txt'
csv_output = '../../training-sets/definitions/sboa-simple.csv'
acronyms, definitions = parse(file_path)
writer_stuff(acronyms, definitions, csv_output)
