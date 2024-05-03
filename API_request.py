import os
import requests
import json
from pathlib import Path
import time

# Constants
API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = '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'  # Secure this in your environment or a config file
CLEANED_TEXT_DIR = 'src/data/cleaned-sec-edgar-filings'
OUTPUT_DIR = 'src/data/output-responses'
REQUEST_INTERVAL = 60  # seconds to wait between requests to manage API rate limit

def make_request(text):
    prompt = """
    "Please provide a comprehensive financial analysis including year-over-year growth, key financial ratios, and a detailed discussion on expenses and revenue sources. Compare these figures to industry averages and discuss any significant deviations."
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": text + prompt}]
    })
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def save_response(response, filename):
    """Save the response data to a JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the output directory exists
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=4)
    print(f"Response saved to {file_path}")

def process_text_files():
    pathlist = Path(CLEANED_TEXT_DIR).rglob('*.txt')  # Find all .txt files recursively
    for path in pathlist:
        file_path = str(path)
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        response = make_request(text_content)
        if response:
            print("Received response:", response)
            # Create a filename from the path to save the response
            response_filename = f"{path.stem}_response.json"
            save_response(response, response_filename)
        time.sleep(REQUEST_INTERVAL)  # Respect the API rate limit

if __name__ == '__main__':
    process_text_files()
