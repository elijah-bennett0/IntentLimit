from transformers import RobertaTokenizer
import torch
from codebert_new import CodeBERTClassifier

# Load model
model = CodeBERTClassifier()
model.load_state_dict(torch.load("codebert_finetuned/pytorch_model.bin", map_location="cpu"))
model.eval()

# Load tokenizer (must match training!)
tokenizer = RobertaTokenizer.from_pretrained("codebert_finetuned")

# Prediction function
def predict(snippet):
    inputs = tokenizer(snippet, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs["logits"]
        pred = torch.argmax(logits, dim=-1).item()
    probs = torch.softmax(logits, dim=-1)
    print(f"Confidence → Safe: {probs[0][0].item():.4f}, Vulnerable: {probs[0][1].item():.4f}")

    return "vulnerable" if pred == 1 else "safe"

# Test
snips = ["""int add(int a, int b) {
    return a + b;
}""","""
void safe_input(int x) {
    if (x > 0 && x < 100) {
        printf("Valid input: %d\n", x);
    }
}""","""
void print_char(char *str, int len) {
    if (len < 256) {
        char buf[256];
        strncpy(buf, str, len);
        buf[len] = '\0';
        puts(buf);
    }
}""","""
void get_username() {
    char username[64];
    fgets(username, sizeof(username), stdin);
    printf("Hello, %s", username);
}""","""
void log_info(const char *msg) {
    char log[100];
    snprintf(log, sizeof(log), "Info: %s", msg);
    puts(log);
}""","""
void safe_deref(int *ptr) {
    if (ptr != NULL) {
        *ptr = 10;
    }
}""","""
void allocate_buffer(size_t size) {
    if (size > 0 && size < 1024) {
        char *buffer = (char *)malloc(size);
        if (buffer) {
            memset(buffer, 0, size);
            free(buffer);
        }
    }
}""","""
void sum_array(int arr[], int len) {
    int sum = 0;
    for (int i = 0; i < len && i < 100; ++i) {
        sum += arr[i];
    }
    printf("Sum: %d\n", sum);
}""","""
void handle_status(int code) {
    switch (code) {
        case 0: puts("OK"); break;
        case 1: puts("Warning"); break;
        case 2: puts("Error"); break;
        default: puts("Unknown"); break;
    }
}""","""
void safe_copy(char *src, size_t len) {
    if (len <= 64) {
        char dest[64];
        memcpy(dest, src, len);
    }
}"""]

for snip in snips:
    print(predict(snip))

