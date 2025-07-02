# quantize_model.py
from codebert_new import CodeBERTClassifier
import torch
import os

# Load original model
model = CodeBERTClassifier()
model.load_state_dict(torch.load("codebert_model/pytorch_model.bin", map_location="cpu"))
model.eval()

# Quantize
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Save the whole quantized model object (not just state_dict)
os.makedirs("codebert_model_quantized", exist_ok=True)
torch.save(quantized_model, "codebert_model_quantized/model.pt")
print("✅ Quantized model saved as full model to: codebert_model_quantized/model.pt")
