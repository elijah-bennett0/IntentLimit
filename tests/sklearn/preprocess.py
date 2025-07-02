import pandas as pd
import numpy as np

# --- Load your raw CSV ---
df = pd.read_csv("juliet_dataset.csv")  # Replace with your actual file

# --- Ensure proper column names ---
assert set(df.columns) >= {"code", "label"}, "CSV must contain 'code' and 'label' columns"

# --- Drop rows with missing or malformed values ---
df = df.dropna(subset=["code", "label"])
df = df[df["label"].isin([0, 1])]

# --- Strip leading/trailing whitespace and newline characters ---
df["code"] = df["code"].astype(str).str.strip()

# --- Drop overly long code snippets (to avoid exceeding CodeBERT 512 token limit) ---
df = df[df["code"].str.len() < 1500]

# --- Optional: Balance the dataset (equal # of 0s and 1s) ---
min_count = df["label"].value_counts().min()
balanced_df = (
    df.groupby("label")
    .apply(lambda x: x.sample(min_count, random_state=42))
    .reset_index(drop=True)
)

# --- Shuffle and save cleaned dataset ---
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
balanced_df.to_csv("juliet_cleaned_balanced.csv", index=False)

print("✅ Preprocessing complete.")
print("Final label distribution:")
print(balanced_df["label"].value_counts())
