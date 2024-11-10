import os
import csv

def parser(content):
    ret = []
    lines = content.splitlines()
    skip_phrases = ["Join us on the last Tuesday", "help@finos.org", "FINOS Community Calendar",
                    "Subscribe", "Edit this page", "View meeting notes", "cdm-collateral-wg+subscribe@lists.finos.org"]
    for x in lines:
        x = x.strip()
        if any(skip_phrase in x for skip_phrase in skip_phrases):
            continue
        if x:
            ret.append(x)
    return ret
def writer_stuff(input_dir, output_file):
    all_entries = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                ret = parser(content)
                entry = {
                    "File Name": filename,
                    "Content": " ".join(ret)
                }
                all_entries.append(entry)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["File Name", "Content"])
        writer.writeheader()
        for entry in all_entries:
            writer.writerow(entry)
input_dir = '../../gen-texts/cdm_docs'
output_file = '../../training-sets/CDM/cdm_training_data.csv'
writer_stuff(input_dir, output_file)
