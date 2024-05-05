import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pathlib import Path
import re

# Ensure you have the necessary NLTK resources downloaded
nltk.download('punkt')
nltk.download('wordnet')

def process_text(text):
    """Apply lemmatization to the text."""
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized)

def extract_numeric_contexts(text, window_size=5):
    """Extract context windows around numeric data in the text."""
    tokens = word_tokenize(text)
    numeric_contexts = []
    numeric_regex = r'\d+[\d,]*\.?\d*'

    for i, token in enumerate(tokens):
        if re.match(numeric_regex, token):
            left_context = tokens[max(i - window_size, 0):i]
            right_context = tokens[i + 1:min(i + window_size + 1, len(tokens))]
            context = left_context + [token] + right_context
            numeric_contexts.append(' '.join(context))

    return ' '.join(numeric_contexts)

def process_files(input_dir, output_dir):
    """Process files from input_dir and save processed contexts to output_dir, mirroring the directory structure."""
    input_path = Path(input_dir)
    for path in input_path.rglob('*.txt'):
        relative_path = path.relative_to(input_path)
        output_path = Path(output_dir) / relative_path
        
        print(f"Processing file: {path}")
        with open(path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        # Process text to get lemmatized and extract numeric contexts
        lemmatized_text = process_text(text_content)
        contexts = extract_numeric_contexts(lemmatized_text)

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(contexts)
        print(f"Processed contexts saved to {output_path}")

# Define paths
CLEANED_TEXT_DIR = 'src/data/cleaned-sec-edgar-filings'
OUTPUT_DIR = 'src/data/processed-numeric-contexts'

if __name__ == '__main__':
    process_files(CLEANED_TEXT_DIR, OUTPUT_DIR)
