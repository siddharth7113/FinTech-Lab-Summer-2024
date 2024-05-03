import os
from bs4 import BeautifulSoup
from pathlib import Path

# Define the root directory where the original filings are stored and the directory to save cleaned text
ROOT_DIRECTORY = 'src/data/sec-edgar-filings'
CLEANED_TEXT_DIR = 'src/data/cleaned-sec-edgar-filings'

# Ensure the directory for cleaned text exists
os.makedirs(CLEANED_TEXT_DIR, exist_ok=True)

# Function to clean and extract text using Beautiful Soup
def clean_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove script, style, and meta tags as they do not contain relevant text
    for script_or_style in soup(["script", "style", "meta"]):
        script_or_style.decompose()

    # Attempt to find the main content div by inspecting common tags used for main content
    # Modify this according to actual document structure observed
    main_content = soup.find('div', attrs={'class': 'document'})
    if not main_content:
        main_content = soup.body  # Fallback to using the entire body if specific div is not found

    # Extracting text and reducing whitespace
    text = ' '.join(main_content.stripped_strings if main_content else [])
    return text

# Function to read file, clean content, and save the cleaned text
def process_file(file_path, output_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        cleaned_text = clean_html(content)
        
        # Construct a new path in the cleaned directory with the same file structure
        relative_path = os.path.relpath(file_path, ROOT_DIRECTORY)
        new_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        
        with open(new_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)
        print(f"Saved cleaned text to {new_path}")
    except Exception as e:
        print(f"Failed to process file {file_path}: {e}")

# Main function to walk through the directory structure and process each filing
def process_filings(root_dir, output_dir):
    pathlist = Path(root_dir).rglob('*.txt')  # Find all .txt files recursively
    for path in pathlist:
        file_path = str(path)
        print(f"Processing file: {file_path}")
        process_file(file_path, output_dir)

if __name__ == '__main__':
    process_filings(ROOT_DIRECTORY, CLEANED_TEXT_DIR)




































# import os
# from bs4 import BeautifulSoup
# from pathlib import Path

# # Define the root directory where original filings are stored and the directory to save cleaned text
# ROOT_DIRECTORY = 'src/data/sec-edgar-filings'
# CLEANED_TEXT_DIR = 'src/data/cleaned-sec-edgar-filings'

# # Ensure the directory for cleaned text exists
# os.makedirs(CLEANED_TEXT_DIR, exist_ok=True)

# # Function to extract text using Beautiful Soup
# def extract_text(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()
#         soup = BeautifulSoup(content, 'html.parser')
#         text = soup.get_text()
#         return text
#     except Exception as e:
#         print(f"Failed to process file {file_path}: {e}")
#         return None
    
# # Function to save the cleaned text to a new file
# def save_cleaned_text(text, original_path):
#     try:
#         # Construct a new path in the cleaned directory with the same file structure
#         relative_path = os.path.relpath(original_path, ROOT_DIRECTORY)
#         new_path = os.path.join(CLEANED_TEXT_DIR, relative_path)
#         os.makedirs(os.path.dirname(new_path), exist_ok=True)
#         with open(new_path, 'w', encoding='utf-8') as file:
#             file.write(text)
#         print(f"Saved cleaned text to {new_path}")
#     except Exception as e:
#         print(f"Failed to save cleaned text for {original_path}: {e}")

# # Main function to process all filings
# def process_filings():
#     pathlist = Path(ROOT_DIRECTORY).rglob('*.txt')  # Find all .txt files recursively
#     for path in pathlist:
#         file_path = str(path)
#         print(f"Processing file: {file_path}")
#         extracted_text = extract_text(file_path)
#         if extracted_text:
#             save_cleaned_text(extracted_text, file_path)

# if __name__ == '__main__':
#     process_filings()