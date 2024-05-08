import os
import requests
from pathlib import Path
import time
import json

# Constants
API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = 'API-KEY-HERE'
CLEANED_TEXT_DIR = 'src/data/pre_processed_data/feature'
OUTPUT_DIR = 'src/output/output-responses'
REQUEST_INTERVAL = 10  # seconds to wait between requests to manage API rate limit

def make_request(text):
    prompt = """Generate a detailed financial analysis for the provided data. Please structure your response in a clear and organized manner..."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": text + prompt}],
        "max_tokens": 4000  # Control the maximum output length
    })
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def save_response(response, output_path):
    os.makedirs(output_path.parent, exist_ok=True)  # Ensure the output directory exists
    with open(output_path, 'w', encoding='utf-8') as f:
        if 'choices' in response and len(response['choices']) > 0:
            text = response['choices'][0].get('message', {}).get('content', '')
            f.write(text)
    print(f"Response saved to {output_path}")

def process_json_files():
    input_path = Path(CLEANED_TEXT_DIR)
    output_path_root = Path(OUTPUT_DIR)
    
    for path in input_path.rglob('*.json'):
        relative_path = path.relative_to(input_path)
        output_path = output_path_root / relative_path
        output_path = output_path.with_suffix('.txt')  # Ensure the file extension is .txt for plain text
        
        # Check if the response file already exists
        if not output_path.exists():
            print(f"Processing file: {path}")
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            text_content = ' '.join([str(value) for key, value in data.items() if isinstance(value, str)])
            response = make_request(text_content)
            if response:
                save_response(response, output_path)
            time.sleep(REQUEST_INTERVAL)  # Respect the API rate limit
        else:
            print(f"Skipping {path} as output already exists.")

if __name__ == '__main__':
    process_json_files()
