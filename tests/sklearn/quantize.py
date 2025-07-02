import torch
from codebert_new import CodeBERTClassifier  # Make sure this matches your class
import os

# Load model
model = CodeBERTClassifier()
model.load_state_dict(torch.load("codebert_model/pytorch_model.bin", map_location="cpu"))
model.eval()

# Quantize to 8-bit (only Linear layers)
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Save quantized model
os.makedirs("codebert_model_quantized", exist_ok=True)
torch.save(quantized_model.state_dict(), "codebert_model_quantized/pytorch_model.bin")

print("✅ Quantized model saved to: codebert_model_quantized/pytorch_model.bin")
