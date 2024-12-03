import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

hf_cache_dir = "/gpfs/u/home/RGCH/RGCHlprt/scratch-shared/hf_cache"  
os.environ['HF_HOME'] = hf_cache_dir
os.environ['HF_DATASETS_CACHE'] = os.path.join(hf_cache_dir, 'datasets')
os.environ['HF_HUB_CACHE'] = hf_cache_dir  
os.environ["HUGGINGFACE_TOKEN"] = "YOUR_HUGGINGFACE_TOKEN"  


model_name = "RG_Model" 

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    cache_dir=hf_cache_dir,
    use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    cache_dir=hf_cache_dir,
    use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def generate_answer(question):
    inputs = tokenizer.encode(question, return_tensors="pt", truncation=True, max_length=512)
    inputs = inputs.to(device)
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=150,
            num_beams=5,
            early_stopping=True
        )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def load_test_data(csv_path):
    df = pd.read_csv(csv_path)
    if 'question' not in df.columns or 'expected_answer' not in df.columns:
        raise ValueError("CSV file must contain 'question' and 'expected_answer' columns.")
    return df

def evaluate_model(test_data):
    total = len(test_data)
    correct = 0
    bleu_scores = []
    smoothing = SmoothingFunction()

    for idx, row in test_data.iterrows():
        question = row['question']
        expected_answer = str(row['expected_answer']).strip()
        generated_answer = generate_answer(question).strip()
        
        print(f"Question {idx+1}: {question}")
        print(f"Expected Answer: {expected_answer}")
        print(f"Generated Answer: {generated_answer}")
        print('-' * 50)
        
        if expected_answer.lower() == generated_answer.lower():
            correct += 1
        
        reference = [expected_answer.split()]
        candidate = generated_answer.split()
        bleu_score = sentence_bleu(reference, candidate, smoothing_function=smoothing.method1)
        bleu_scores.append(bleu_score)
    
    accuracy = correct / total * 100
    average_bleu = sum(bleu_scores) / total * 100
    print(f"Model Accuracy (Exact Match): {accuracy:.2f}% ({correct}/{total} correct)")
    print(f"Average BLEU Score: {average_bleu:.2f}%")

if __name__ == "__main__":
    test_csv_path = "test_set.csv"  
    test_data = load_test_data(test_csv_path)
    evaluate_model(test_data)
