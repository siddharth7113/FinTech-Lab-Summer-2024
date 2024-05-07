import os
from pathlib import Path

# Define the directory containing the output text files
output_dir = Path('src/data/output/output-responses')
combined_dir = Path('src/output/pre-analysis_combined')
combined_dir.mkdir(exist_ok=True)  # Ensure the combined directory exists

def combine_firm_files():
    # Dictionary to hold combined texts for each firm
    firm_texts = {}

    # Traverse through all text files in the output directory
    for file_path in output_dir.rglob('full-submission_features.txt'):
        # Debugging: Print the path to see what's being captured
        print(f"Current file path: {file_path}")
        print(f"Path parts: {file_path.parts}")

        # Extract the firm name based on the file structure
        # src/data/output-responses/<FIRM_NAME>/.../full-submission_features.txt
        # Ensure this index corresponds correctly to the firm name part in the path
        if len(file_path.parts) >= 5:  # Check there are enough parts
            firm_name = file_path.parts[3]  # Index where the firm name appears, adjusted if needed
        else:
            continue  # Skip if the path is not deep enough to contain a firm name

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Append the text to the corresponding firm's entry in the dictionary
        if firm_name in firm_texts:
            firm_texts[firm_name] += "\n" + text
        else:
            firm_texts[firm_name] = text

    # Write combined texts to new files, one per firm
    for firm_name, text in firm_texts.items():
        combined_file_path = combined_dir / f"{firm_name}_combined.txt"
        with open(combined_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Combined file created for firm {firm_name}: {combined_file_path}")

if __name__ == '__main__':
    combine_firm_files()
