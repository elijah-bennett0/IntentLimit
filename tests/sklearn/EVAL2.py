print("✅ Running custom evaluation script using DataLoader")

import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import RobertaTokenizer
import pandas as pd
from sklearn.metrics import classification_report
from codebert_new import CodeBERTClassifier  # Your model definition

# --- Device ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# --- Load Model and Tokenizer ---
model = CodeBERTClassifier()
model.load_state_dict(torch.load("./codebert_model/pytorch_model.bin", map_location=device))
model.to(device)
model.eval()

tokenizer = RobertaTokenizer.from_pretrained("./codebert_model")

# --- Load and Preprocess Dataset ---
df = pd.read_csv("devign_test_only.csv")
# Fix label format: convert space-separated string to array
import numpy as np

def extract_single_label(value):
    try:
        value = str(value).replace('\n', ' ').replace('\t', ' ')
        arr = np.fromstring(value.strip("[]"), sep=' ')
        if arr.size == 0:
            raise ValueError("Empty label array.")
        return int(np.argmax(arr))
    except Exception:
        raise ValueError(f"Invalid label format: {value}")

df['label'] = df['label'].apply(extract_single_label)
df = df[df['label'].isin([0, 1])]

if df.empty:
    raise ValueError("DataFrame is empty after filtering. Check label values or preprocessing.")

# Rename and truncate columns
df = df[['func', 'label']]
df = df.rename(columns={'func': 'code'})
df = df[df['code'].str.len() < 1500]  # Optional: truncate long code

# --- Tokenization ---
encodings = tokenizer(
    list(df['code']),
    padding="max_length",
    truncation=True,
    max_length=512,
    return_tensors="pt"
)

labels = torch.tensor(df['label'].values)

# --- Create DataLoader ---
dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'], labels)
dataloader = DataLoader(dataset, batch_size=64)

# --- Run Evaluation ---
all_preds = []
all_labels = []

with torch.no_grad():
    for batch in dataloader:
        input_ids, attention_mask, batch_labels = [b.to(device) for b in batch]
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs["logits"] if isinstance(outputs, dict) else outputs
        predictions = torch.argmax(logits, dim=-1)
        all_preds.extend(predictions.cpu().numpy())
        all_labels.extend(batch_labels.cpu().numpy())

# --- Report Results ---
print(classification_report(all_labels, all_preds))
