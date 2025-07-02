import torch
import numpy as np
import torch.nn as nn
import pandas as pd
from datasets import Dataset, load_dataset, concatenate_datasets
from transformers import RobertaTokenizer, RobertaModel, Trainer, TrainingArguments
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_class_weight

# 1. Load local dataset
df_local = pd.read_csv("dataset.csv")
df_local = df_local[['code', 'label']]
df_local = df_local[df_local['code'].str.len() < 1500]

# 2. Load BigVul dataset from HuggingFace
hf_raw = load_dataset("bstee615/bigvul")

def process_bigvul(example):
    if example["vul"] == 1:
        return {"code": example["func_before"], "label": 1}
    else:
        return {"code": example["func_before"], "label": 0}

hf_dataset = hf_raw["train"].map(process_bigvul)
hf_dataset = hf_dataset.filter(lambda x: x["code"] is not None and len(x["code"]) < 1500)

# Convert HuggingFace dataset to pandas, align schema
df_hf = pd.DataFrame(hf_dataset)
df_hf = df_hf[['code', 'label']]
df_hf['label'] = df_hf['label'].astype(int)

# Combine datasets
df = pd.concat([df_local, df_hf], ignore_index=True)

# Compute class weights
class_weights = compute_class_weight(class_weight="balanced", classes=np.array([0, 1]), y=df['label'].values)
class_weights = torch.tensor(class_weights, dtype=torch.float)

# 3. Tokenization
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")

def tokenize(batch):
    return tokenizer(batch['code'], padding="max_length", truncation=True, max_length=512)

dataset = Dataset.from_pandas(df)
dataset = dataset.map(tokenize, batched=True)
dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

# 4. Train/test split
train_test = dataset.train_test_split(test_size=0.2, seed=42)
train_ds = train_test['train']
test_ds = train_test['test']

# 5. CodeBERT Model
class CodeBERTClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = RobertaModel.from_pretrained("microsoft/codebert-base")
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(self.bert.config.hidden_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        logits = self.classifier(pooled_output)

        loss = None
        if labels is not None:
            loss_fn = nn.CrossEntropyLoss(weight=class_weights.to(input_ids.device))
            loss = loss_fn(logits, labels)

        return {"loss": loss, "logits": logits} if loss is not None else {"logits": logits}

model = CodeBERTClassifier()

# 6. Training config
training_args = TrainingArguments(
    output_dir="./codebert_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=10,  # ← changed to 10
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    logging_dir="./logs"
)

# 7. Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = torch.tensor(logits).argmax(-1).numpy()
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

# 8. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    compute_metrics=compute_metrics,
)

trainer.train()

# 9. Save
torch.save(model.state_dict(), "./codebert_model/pytorch_model.bin")
tokenizer.save_pretrained("./codebert_model")

# 10. Evaluation
preds = trainer.predict(test_ds)
y_true = preds.label_ids
y_pred = preds.predictions.argmax(-1)

print("\n[+] Classification Report:")
print(classification_report(y_true, y_pred))
