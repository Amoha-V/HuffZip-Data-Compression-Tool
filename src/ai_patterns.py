
from transformers import pipeline

def analyze_patterns(data):
    # Use BART for text generation
    analyzer = pipeline(
        "text-generation",
        model="facebook/bart-base",  # BART model
        framework="pt",  # Force PyTorch backend
        use_auth_token=""  # Replace with your token
    )
    patterns = analyzer(data, max_length=50)
    return patterns