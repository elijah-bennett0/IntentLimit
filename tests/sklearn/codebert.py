import torch
import pandas as pd
from datasets import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Load and clean dataset
df = pd.read_csv("devign_processed.csv")
df = df[['code', 'label']]
df = df[df['code'].str.len() < 1500]  # Optional: remove very long functions

# 2. Tokenize using CodeBERT
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")

def tokenize(batch):
    return tokenizer(batch['code'], padding="max_length", truncation=True, max_length=256)

# 3. Convert to HuggingFace Dataset
dataset = Dataset.from_pandas(df)
dataset = dataset.map(tokenize, batched=True)
dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

# 4. Split into train/test sets
train_test = dataset.train_test_split(test_size=0.2, seed=42)
train_ds = train_test['train']
test_ds = train_test['test']

# 5. Load CodeBERT model for binary classification
model = RobertaForSequenceClassification.from_pretrained("microsoft/codebert-base", num_labels=2)

# 6. Training configuration
training_args = TrainingArguments(
    output_dir="./codebert_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    load_best_model_at_end=True,
)

# 7. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
)

# 8. Train model
trainer.train()

# 9. Evaluate
preds_output = trainer.predict(test_ds)
y_true = preds_output.label_ids
y_pred = preds_output.predictions.argmax(-1)

print("\n[+] Classification Report:")
print(classification_report(y_true, y_pred))

# 10. Save model/tokenizer
model.save_pretrained("./codebert_model")
tokenizer.save_pretrained("./codebert_model")

# 11. Inference function

def predict_code_snippet(code_snippet):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()
    model.to(device)  # Ensure model is on the right device

    inputs = tokenizer(code_snippet, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # Move input tensors to same device

    with torch.no_grad():
        output = model(**inputs)
        prediction = torch.argmax(output.logits, dim=1).item()
        return "VULNERABLE" if prediction == 1 else "SAFE"

# 12. Test prediction
example = "strcpy(buffer, input);"
print(f"\n[+] Prediction for: {example}")
print(f"    => {predict_code_snippet(example)}")
