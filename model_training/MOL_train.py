import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset
import os
import torch

hf_cache_dir = "/gpfs/u/home/RGCH/RGCHlprt/scratch-shared/hf_cache"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['HF_HOME'] = hf_cache_dir
os.environ['HF_DATASETS_CACHE'] = os.path.join(hf_cache_dir, 'datasets')
os.environ['HF_HUB_CACHE'] = hf_cache_dir  
os.environ["HUGGINGFACE_TOKEN"] = "YOUR_HUGGINGFACE_TOKEN"  

model_name = "meta-llama/Llama-3.1-8B" 

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
model.to('cuda')

def prepare_dataset(csv_path, license_text_dir):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    input_texts = []
    target_texts = []
    
    for idx, row in df.iterrows():
        file_name = row['File Name']
        license_name = row['License Name']
        

        license_file_path = os.path.join(license_text_dir, file_name)
        

        try:
            with open(license_file_path, 'r', encoding='utf-8') as f:
                license_text = f.read()
        except FileNotFoundError:
            print(f"File not found: {license_file_path}")
            continue
        

        input_text = license_text  
        target_text = license_name  
        
        input_texts.append(input_text)
        target_texts.append(target_text)

    data = {'input_text': input_texts, 'target_text': target_texts}
    dataset_df = pd.DataFrame(data)
    

    dataset = Dataset.from_pandas(dataset_df)
    
    dataset = dataset.train_test_split(test_size=0.1)
    
    return dataset


data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

args = TrainingArguments(
    output_dir="output_license_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    fp16=True,
    per_device_train_batch_size=1,  
    per_device_eval_batch_size=1,
    push_to_hub=True,
    hub_token="YOUR_HUGGINGFACE_TOKEN", 
    hub_model_id='YOUR_USERNAME/License_Name_Generator', 
    gradient_checkpointing=True,
    remove_unused_columns=False,
    predict_with_generate=True
)

dataset = prepare_dataset("licenses_output.csv", "path_to_files")

trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=args,
    data_collator=data_collator,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"]
)

trainer.train()
