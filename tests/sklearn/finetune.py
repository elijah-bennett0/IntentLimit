import torch
import numpy as np
import pandas as pd
import torch.nn as nn
from datasets import Dataset
from transformers import (
    RobertaTokenizer,
    RobertaModel,
    RobertaConfig,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support

# --- Model Definition ---
class CodeBERTClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        config = RobertaConfig.from_pretrained(
            "microsoft/codebert-base",
            hidden_dropout_prob=0.3,
            attention_probs_dropout_prob=0.3,
        )
        self.bert = RobertaModel.from_pretrained("microsoft/codebert-base", config=config)
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(config.hidden_size, 256),
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

# --- Main Logic ---
if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv("Vulnerability_Fragment_Dataset.csv")
    df = df[['code', 'label']]
    df = df[df['code'].str.len() < 1500]

    # Compute class weights
    class_weights = compute_class_weight(class_weight="balanced", classes=np.array([0, 1]), y=df['label'].values)
    class_weights = torch.tensor(class_weights, dtype=torch.float)

    # Tokenizer
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")

    def tokenize(batch):
        return tokenizer(batch['code'], padding="max_length", truncation=True, max_length=512)

    dataset = Dataset.from_pandas(df)
    dataset = dataset.map(tokenize, batched=True)
    dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

    # Stratified train/val/test split
    train_test = dataset.train_test_split(test_size=0.2, seed=42)
    train_valid = train_test['train'].train_test_split(test_size=0.1, seed=42)
    train_ds = train_valid['train']
    val_ds = train_valid['test']
    test_ds = train_test['test']

    # Model
    model = CodeBERTClassifier()

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./codebert_finetuned",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        learning_rate=2e-5,
        weight_decay=0.01,
        warmup_steps=100,
        lr_scheduler_type="linear",
        load_best_model_at_end=True,
        logging_dir="./logs",
        logging_steps=10,
        save_total_limit=2,
        metric_for_best_model="eval_f1",
        greater_is_better=True,
    )

    # Metrics
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = torch.tensor(logits).argmax(-1).numpy()
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    # Train
    trainer.train()

    # Save final model + tokenizer
    torch.save(model.state_dict(), "./codebert_finetuned/pytorch_model.bin")
    tokenizer.save_pretrained("./codebert_finetuned")

    # Final Evaluation
    preds = trainer.predict(test_ds)
    y_true = preds.label_ids
    y_pred = preds.predictions.argmax(-1)
    print("\n🔎 Classification Report:")
    print(classification_report(y_true, y_pred))
