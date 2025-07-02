import torch
import torch.nn as nn
from transformers import RobertaTokenizer
from codebert_new import CodeBERTClassifier  # Update this import path if needed

# Load tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained("codebert_model")
model = CodeBERTClassifier()
model.load_state_dict(torch.load("codebert_model/pytorch_model.bin", map_location="cpu"))
model.eval()

# Function to classify code
def classify_code(snippet: str):
    # Tokenize the code
    inputs = tokenizer(snippet, return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    
    # Run model
    with torch.no_grad():
        outputs = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
        logits = outputs["logits"]
        predicted_class = torch.argmax(logits, dim=1).item()
        confidence = torch.softmax(logits, dim=1)[0, predicted_class].item()
    
    label_str = "🔒 Safe" if predicted_class == 0 else "⚠️ Vulnerable"
    return label_str, confidence

# === EXAMPLE USAGE ===

code_snippets = [
    """void safe_copy(char *input) {
        char buffer[20];
        strncpy(buffer, input, sizeof(buffer) - 1);
        buffer[19] = '\\0';
    }""",
    
    """void vulnerable_copy(char *input) {
        char buffer[10];
        strcpy(buffer, input);  // unsafe
    }""",

    """int main() {
        char user[50];
        fgets(user, sizeof(user), stdin);
        printf(user);  // format string vulnerability
        return 0;
    }"""
]

# Run inference
for i, snippet in enumerate(code_snippets, 1):
    label, confidence = classify_code(snippet)
    print(f"\nSnippet #{i}:\n{snippet.strip()}\nPrediction: {label} (Confidence: {confidence:.2f})")
