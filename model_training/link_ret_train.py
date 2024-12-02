# train_generated_question_set.py
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

def prepare_dataset(csv_path):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    dataset = Dataset.from_pandas(df.rename(columns={"question": "input_text", "answer": "target_text"}))
    return dataset.train_test_split(test_size=0.1)

data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

args = TrainingArguments(
    output_dir="output_generated_question_set",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    fp16=True,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    push_to_hub=True,
    hub_token="YOUR_HUGGINGFACE_TOKEN",
    hub_model_id='Aabe03/QA_Challenge_Generated',
    gradient_checkpointing=True,
    remove_unused_columns=False,
    predict_with_generate=True
)

dataset = prepare_dataset("generated_question_set.csv")

trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=args,
    data_collator=data_collator,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"]
)

trainer.train()
