import os
import csv

JULIET_ROOT = "C/testcases"  # CHANGE THIS

def extract_code_and_label(filepath):
    with open(filepath, 'r', encoding='latin-1', errors='ignore') as f:
        code = f.read()

    label = None

    # Infer from filename or content
    lower_path = filepath.lower()
    if "bad" in lower_path or "flaw" in code.lower():
        label = 1
    elif "good" in lower_path or "fix" in code.lower():
        label = 0
    else:
        return None, None  # Skip unclear cases

    # Basic cleanup (optional)
    code = code.strip().replace('\r\n', '\n').replace('\t', '    ')
    return code, label

def collect_examples(root_dir):
    examples = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".c") or file.endswith(".cpp"):
                path = os.path.join(root, file)
                code, label = extract_code_and_label(path)
                if code and label is not None:
                    examples.append({"code": code, "label": label})
    return examples

def save_to_csv(data, out_path="juliet_dataset.csv"):
    with open(out_path, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["code", "label"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    print("🔍 Parsing Juliet test suite...")
    examples = collect_examples(JULIET_ROOT)
    print(f"✅ Extracted {len(examples)} examples.")

    print("💾 Writing to CSV...")
    save_to_csv(examples)
    print("📄 Saved to juliet_dataset.csv")
