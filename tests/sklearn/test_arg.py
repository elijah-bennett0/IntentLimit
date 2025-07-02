from transformers import TrainingArguments

args = TrainingArguments(
    output_dir="./test_out",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8
)

print("✅ TrainingArguments initialized successfully.")
