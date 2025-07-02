import pandas as pd

df = pd.read_csv("juliet_dataset.csv")

# Check structure
print(df.head())
print(df.columns)

# Check for NaNs or empty entries
assert df['code'].notnull().all(), "❌ Some code entries are missing."
assert df['label'].isin([0, 1]).all(), "❌ Labels must be only 0 or 1."

# Check for long entries
print("Longest snippet length:", df['code'].str.len().max())

# Optional: Drop very long entries
df = df[df['code'].str.len() < 1500]
