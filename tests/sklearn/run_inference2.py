# run_inference.py
import torch
import warnings
from transformers import RobertaTokenizer
from codebert_new import CodeBERTClassifier

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load tokenizer
tokenizer = RobertaTokenizer.from_pretrained("codebert_model_quantized")

# Load full quantized model object
torch.serialization.add_safe_globals({"codebert_new.CodeBERTClassifier": CodeBERTClassifier})

model = torch.load("codebert_model_quantized/model.pt", map_location="cpu", weights_only=False)
model.eval()

# Sample code snippet
code_snippets = ["""
void overflow(char *input) {
    char buf[8];
    strcpy(buf, input);
}""","""
void get_input() {
    char buffer[100];
    gets(buffer); // unsafe
}""","""
void allocate(int size) {
    int total = size * 4;
    char *buffer = (char *)malloc(total);
    // ... use buffer
}""","""
void log_msg(char *user_input) {
    printf(user_input); // unsafe if input is not sanitized
}""","""
void copy_safe(char *input) {
    char buf[16];
    strncpy(buf, input, sizeof(buf) - 1);
    buf[15] = '\0';
}""","""
void get_input() {
    char buffer[100];
    fgets(buffer, sizeof(buffer), stdin);
}""","""
void log_safe() {
    printf("Program started.\n");
}""","""
void allocate(int size) {
    if (size > 0 && size < 1000) {
        char *buffer = (char *)malloc(size);
        if (buffer != NULL) {
            // use buffer
            free(buffer);
        }
    }
}"""]

for snip in code_snippets:
# Tokenize
	inputs = tokenizer(
	snip,
	return_tensors="pt",
	padding="max_length",
	truncation=True,
	max_length=512
	)

# Inference
	with torch.no_grad():
		outputs = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
		logits = outputs["logits"] if isinstance(outputs, dict) else outputs
		prediction = torch.argmax(logits, dim=-1).item()

	print("Prediction:", "✅ Safe" if prediction == 0 else "⚠️ Vulnerable")
