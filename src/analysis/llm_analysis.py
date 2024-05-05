# import requests
# import json
# from pathlib import Path

# # Constants
# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# OPENROUTER_API_KEY = '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'

# INPUT_DIR = 'src/analysis/pre-analysis_combined'
# CSV_OUTPUT_DIR = 'src/analysis/csv'
# CODE_OUTPUT_DIR = 'src/analysis/code'
# TEXT_OUTPUT_DIR = 'src/analysis/text'

# def make_api_call(text_content):
#     prompt = f"""
#     Analyze the financial data provided and give a json file  containing csv,python and text:
#     1. Generate a CSV file with key financial metrics for plotting.
#     2. Provide Python code for creating plots and animations based on the CSV.
#     3. Provide key financial insights in text format that can be displayed on a web page.
#     """
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "model": "nousresearch/nous-capybara-7b:free",
#         "messages": [
#             {"role": "user", "content": text_content + prompt} 
#         ]
#     })
#     response = requests.post(API_URL, headers=headers, json=data)
#     return response.json()

# def save_output(data, output_path, file_type):
#     Path(output_path).mkdir(parents=True, exist_ok=True)
#     file_path = Path(output_path) / f"{file_type}.txt"
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(data)
#     print(f"Output saved to {file_path}")

# def process_files():
#     input_path = Path(INPUT_DIR)
#     for text_file in input_path.rglob('*.txt'):
#         print(f"Processing: {text_file}")
#         with open(text_file, 'r', encoding='utf-8') as file:
#             text_content = file.read()

#         response = make_api_call(text_content)
#         if response:
#             # Assuming the API returns a structured JSON with keys for different types of outputs
#             if 'csv' in response:
#                 save_output(response['csv'], CSV_OUTPUT_DIR, text_file.stem)
#             if 'code' in response:
#                 save_output(response['code'], CODE_OUTPUT_DIR, text_file.stem)
#             if 'text' in response:
#                 save_output(response['text'], TEXT_OUTPUT_DIR, text_file.stem)

# if __name__ == '__main__':
#     process_files()
