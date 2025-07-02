from datasets import load_dataset
import pandas as pd

# Load directly from Hugging Face hub (no local files needed)
dataset = load_dataset("DetectVul/devign")

# Combine all splits
df_train = dataset["train"].to_pandas()
df_test = dataset["test"].to_pandas()
df_val = dataset["validation"].to_pandas()
df = pd.concat([df_train, df_test, df_val], ignore_index=True)

# Clean and rename
df['func'] = df['func'].str.replace(r'\s+', ' ', regex=True)
df = df.rename(columns={'func': 'code', 'target': 'label'})

# Save to CSV
df.to_csv("devign_processed.csv", index=False)
print(f"[+] Done! Saved {len(df)} samples to devign_processed.csv")
