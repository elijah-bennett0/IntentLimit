import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import RobertaTokenizer
import pandas as pd
from sklearn.metrics import classification_report
from final_codebert import CodeBERTClassifier  # Your model definition

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
df = df[['code', 'label']]
df = df[df['code'].str.len() < 1500]  # Optional truncation

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
        logits = outputs.logits if hasattr(outputs, "logits") else outputs
        predictions = torch.argmax(logits, dim=-1)
        all_preds.extend(predictions.cpu().numpy())
        all_labels.extend(batch_labels.cpu().numpy())

# --- Report Results ---
print(classification_report(all_labels, all_preds))
