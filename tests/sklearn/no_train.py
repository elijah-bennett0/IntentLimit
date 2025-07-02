import torch
from transformers import RobertaTokenizer
from model import CodeBERTClassifier  # Assuming you saved the class definition in model.py

# Load model and tokenizer
model_path = "./codebert_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize model architecture and load weights
model = CodeBERTClassifier()
model.load_state_dict(torch.load(f"{model_path}/pytorch_model.bin", map_location=device))
model.to(device)
model.eval()

# Load tokenizer
tokenizer = RobertaTokenizer.from_pretrained(model_path)

def predict_code_snippet(code_snippet):
    inputs = tokenizer(code_snippet, return_tensors="pt", padding=True, truncation=True, max_length=256)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs["logits"]
        prediction = torch.argmax(logits, dim=1).item()
    
    return "VULNERABLE" if prediction == 1 else "SAFE"

# === Example Usage ===
if __name__ == "__main__":
    examples = [
        "strcpy(buffer, input);",
        "printf(\"Hello, world!\");",
        "memcpy(dst, src, len);",
        "int safe = 1;"
    ]

    print("[+] Code Vulnerability Predictions:\n")
    for code in examples:
        result = predict_code_snippet(code)
        print(f"Code: {code}\nResult: {result}\n")
