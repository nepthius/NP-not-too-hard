from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch
import os
import torch.distributed as dist


hf_cache_dir = "/gpfs/u/home/RGCH/RGCHlprt/scratch-shared/hf_cache"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['HF_HOME'] = hf_cache_dir
os.environ['HF_DATASETS_CACHE'] = os.path.join(hf_cache_dir, 'datasets')
os.environ['HF_HUB_CACHE'] = hf_cache_dir  


os.environ["HUGGINGFACE_TOKEN"] = "YOUR_HUGGINGFACE_TOKEN"

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

os.environ["NCCL_DEBUG"] = "INFO"
os.environ["NCCL_DEBUG_SUBSYS"] = "ALL"
os.environ["NCCL_IB_TIMEOUT"] = "22" 
os.environ["NCCL_P2P_LEVEL"] = "NVL"
os.environ["NCCL_SOCKET_IFNAME"] = "^lo,docker0" 
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
os.environ["OMP_NUM_THREADS"] = "1"

print("CUDA available:", torch.cuda.is_available())
print("Number of GPUs:", torch.cuda.device_count())


if 'LOCAL_RANK' in os.environ:
    dist.init_process_group(backend='nccl')
    local_rank = int(os.environ['LOCAL_RANK'])
    torch.cuda.set_device(local_rank)
    device = torch.device('cuda', local_rank)
    print(f"Local rank: {local_rank}, device: {device}")
else:
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")


model_name = "meta-llama/Llama-3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    cache_dir=hf_cache_dir,
    use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=hf_cache_dir,
    use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
)
model.to(device)
tokenizer.pad_token = tokenizer.eos_token

print("Loading dataset...")
dataset = load_dataset("text", data_files={"train": "cleaned_texts/*.txt"}, cache_dir=hf_cache_dir)
print("Dataset loaded.")
print("Splitting dataset into train and test sets...")
dataset = dataset["train"].train_test_split(test_size=0.1)
print("Dataset split completed.")


max_length = 256
stride = 64

def tokenize_function(examples):
    texts = examples["text"]
    texts = [text if text is not None else "" for text in texts]
    return tokenizer(
        texts,
        max_length=max_length,
        truncation=True,
        stride=stride,
        padding="max_length"
    )

# Tokenize dataset
print("Tokenizing dataset...")
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["text"],
    num_proc=1  
)
print("Tokenization completed.")
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
args = TrainingArguments(
    gradient_accumulation_steps=8,
    output_dir="output_dir",
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
    hub_model_id='Aabe03/Regulation_Challenge_AA',
    gradient_checkpointing=True,
    deepspeed="ds_config.json",
    remove_unused_columns=False,
    ddp_find_unused_parameters=False  
)


trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=args,
    data_collator=data_collator,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"]
)

trainer.train()
