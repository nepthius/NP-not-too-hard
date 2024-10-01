import fitz
import tiktoken

#get text from pdfs
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")  #grabs text stuff
    return text

#use titoken for token count...
def count_tokens(text, model_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    return len(tokens)

#read pdf and get tokens using other funcs
def count_tokens_in_pdf(pdf_path, model_name="gpt-4"):
    
    text = extract_text_from_pdf(pdf_path)
    num_tokens = count_tokens(text, model_name)
    
    return num_tokens

pdf_file_path = "../CFA/CFA1/dataset/CFA1-mass.pdf"

#prints tokens
token_count = count_tokens_in_pdf(pdf_file_path)
print(f"The PDF file '{pdf_file_path}' contains {token_count} tokens.")




