import os
import requests
from pathlib import Path
import time
import json

# Constants
API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = "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"
COMBINED_TEXT_DIR = 'src/output/pre-analysis_combined'
OUTPUT_DIR = 'src/analysis/csv'
REQUEST_INTERVAL = 10  # Interval in seconds between requests to manage API rate limit

def make_request(text_content):
    prompt = """
    Provide a year-wise breakdown of all financial points which could be later used to convert 
    into csv using regex in python,make sure the information is available for  all the years
    present between 1995-2023(Ensure everything is complete.)
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": text_content + prompt}]
    })
    print("Sending request to LLM...")
    response = requests.post(API_URL, headers=headers, data=data)
    print("Response status code:", response.status_code)
    if response.status_code == 200:
        try:
            print("Successfully received JSON response")
            return response.json()
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            return None
    else:
        print("Failed request with status code: {response.status_code}")
        print("Response body:", response.text)
        return None

def save_response(response, output_path):
    print(f"Preparing to save the summary and insights at: {output_path}")
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as file:
        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0].get('message', {}).get('content', '')
            file.write(content)
    print(f"Summary and insights saved to {output_path}")

def process_combined_files():
    input_path = Path(COMBINED_TEXT_DIR)
    output_path_root = Path(OUTPUT_DIR)
    
    for path in input_path.rglob('*.txt'):
        relative_path = path.relative_to(input_path)
        output_path = output_path_root / relative_path
        output_path = output_path.with_suffix('.txt')

        if not output_path.exists():
            print(f"Processing file: {path}")
            with open(path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            
            response = make_request(text_content)
            if response:
                save_response(response, output_path)
            else:
                print(f"No valid response received or failed to save for {path.stem}")
            time.sleep(REQUEST_INTERVAL)
        else:
            print(f"Skipping {path} as output already exists.")

if __name__ == '__main__':
    process_combined_files()
