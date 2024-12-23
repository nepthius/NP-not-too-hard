import os
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, DatasetDict

MODEL_NAME = "path/to/llama-8b"
OUTPUT_DIR = "./fine_tuned_llama"
DATASET_PATH = "path/to/dataset"
tokenizer = LlamaTokenizer.from_pretrained(MODEL_NAME)
model = LlamaForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
model = model.half()

def preprocess_data(examples):
    """Preprocess the dataset for the specific tasks."""
    task_map = {
        "Abbreviation Recognition Task": "Expand the following acronym into its full form: {acronym}. Answer:",
        "Definition Recognition Task": "Define the following term: {regulatory_term}. Answer:",
        "Named Entity Recognition (NER) Task": "Given the following text, only list the following for each: specific Organizations, Legislations, Dates, Monetary Values, and Statistics: {input_text}.",
        "Question Answering Task": "Provide a concise answer to the following question: {detailed_question}? Answer:",
        "Link Retrieval Task": "Provide a link for ____ law, Write in the format of ('{Law}: {Link}' or '{Law}: Not able to find a link for the law')",
        "Certificate Question Task": "(This context is used for the question that follows: {context}). Please answer the following question with only the letter and associated description of the correct answer choice: {question}. Answer:",
        "XBRL Analytics Task": "Provide the exact answer to the following question: {detailed_question}? Answer:",
        "Common Domain Model (CDM) Task": "Provide a concise answer to the following question related to Financial Industry Operating Network's (FINOS) Common Domain Model (CDM): {detailed_question}? Answer:",
        "Model Openness Framework (MOF) Licenses Task": "Provide a concise answer to the following question about MOF's licensing requirements: {detailed_question}? Answer:"
    }

    task_type = examples["task_type"]

    sample_data = {
        "acronym": "SEC",
        "regulatory_term": "Financial Stability Oversight Council",
        "input_text": "The SEC fined multiple organizations on January 10, 2023, totaling $3 million.",
        "detailed_question": "What is the role of the SEC in financial regulation?",
        "Law": "Sarbanes-Oxley Act",
        "context": "The Sarbanes-Oxley Act outlines regulations to ensure transparency in financial reporting.",
        "question": "Which of the following is a provision of the Sarbanes-Oxley Act? (A) Transparency requirements, (B) Increased executive pay, (C) Reduced penalties for fraud.",
        "expected_output": "A: Transparency requirements"
    }

    input_data = task_map[task_type].format(**sample_data)

    return {
        "input_ids": tokenizer(input_data, truncation=True, padding="max_length", max_length=512)["input_ids"],
        "attention_mask": tokenizer(input_data, truncation=True, padding="max_length", max_length=512)["attention_mask"],
        "labels": tokenizer(sample_data["expected_output"], truncation=True, padding="max_length", max_length=512)["input_ids"]
    }

#load and split up the data
dataset = load_dataset("json", data_files=DATASET_PATH)
dataset = dataset.map(preprocess_data, batched=True)
data = DatasetDict({
    "train": dataset["train"],
    "validation": dataset["validation"]
})

#basic arg stuff
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=3,
    learning_rate=5e-5,
    weight_decay=0.01,
    logging_dir=f"{OUTPUT_DIR}/logs",
    logging_steps=10,
    save_total_limit=2,
    fp16=True,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    greater_is_better=False
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=data["train"],
    eval_dataset=data["validation"],
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
eval_results = trainer.evaluate()
print("Evaluation Results.....", eval_results)

#predict
def generate_predictions(input_text):
    """Generate predictions for given input text."""
    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
sample_input = "Expand the following acronym into its full form: SEC. Answer:"
print(generate_predictions(sample_input))
