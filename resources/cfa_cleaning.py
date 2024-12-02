import fitz  # PyMuPDF
import re
import os


#remove all unneeded text in textbooks that would be destructive to model
def remove_headers(text):
    pattern = r'^\s*Chapter\s+\d+.*$'
    cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
    return cleaned_text

def remove_footers(text):
    pattern = r'©.*For candidate use only\. Not for distribution\.\s*$'
    cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
    return cleaned_text

def remove_page_numbers(text):
    pattern = r'^\s*(\d+|[ivxlcdm]+)\s*$'
    cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
    return cleaned_text

def remove_repetitive_phrases(text):
    phrases = [
        r'The Time Value of Money',
        r'Quantitative Methods',
        r'How to Use the CFA Program Curriculum',
    ]
    for phrase in phrases:
        pattern = rf'^\s*{phrase}\s*$'
        text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
    return text

def remove_trademarks(text):
    pattern = r'®|™'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def remove_bullets_and_numbers(text):
    pattern = r'^\s*[\u2022\u2023\u25E6\u2043\u2219\-–—]\s*|\d+\.\s+'
    cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return cleaned_text

def clean_whitespace(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def clean_text(text):
    text = remove_headers(text)
    text = remove_footers(text)
    text = remove_page_numbers(text)
    text = remove_repetitive_phrases(text)
    text = remove_trademarks(text)
    text = remove_bullets_and_numbers(text)
    text = clean_whitespace(text)
    return text

def extract_and_clean_text(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ''
    for page_num, page in enumerate(doc):
        text = page.get_text()
        cleaned_text = clean_text(text)
        all_text += cleaned_text + ' '
    return all_text.strip()

def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

pdf_paths = [
    'CFA1-mass.pdf',
    'CFA2-1.pdf',
    'CFA2-2.pdf',
    'CFA2-3.pdf',
    'CFA2-4.pdf',
    'CFA2-5.pdf',
    'CFA2-6.pdf',
    'cfa3-MASS(2023).pdf'
]

output_dir = 'cleaned_texts'
os.makedirs(output_dir, exist_ok=True)

for pdf_path in pdf_paths:
    print(f"Processing {pdf_path}...")
    cleaned_text = extract_and_clean_text(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = os.path.join(output_dir, f"{base_name}_cleaned.txt")
    save_text_to_file(cleaned_text, output_file)
    print(f"Cleaned text saved to {output_file}")

print("Text extraction and cleaning complete.")
