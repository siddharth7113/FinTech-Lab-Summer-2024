import re
import csv
from pathlib import Path

# Define the path to the directory containing the text files
input_dir = Path('src/analysis/csv')

# Regex patterns to extract financial data
patterns = {
    'year': r'\d{4}',
    'revenue': r'Revenue:\s*\$(\d+\.?\d*)\s*billion',
    'net_income': r'Net Income:\s*\$(\d+\.?\d*)\s*million',
    'total_assets': r'Total assets:\s*\$(\d+\.?\d*)\s*million',
    'total_liabilities': r'Total liabilities:\s*\$(\d+\.?\d*)\s*million'
}

# Process each file in the directory and create a separate CSV for each
for file_path in input_dir.glob('*.txt'):
    output_file = input_dir / f"{file_path.stem}_financial_data.csv"
    
    # Prepare to write to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['year', 'revenue', 'net_income', 'total_assets', 'total_liabilities']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"Processing {file_path.name}")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Extract data from content
            data = {key: re.findall(pattern, content) for key, pattern in patterns.items()}
            
            # Write data to CSV file
            for i, year in enumerate(data['year']):
                writer.writerow({
                    'year': year,
                    'revenue': data['revenue'][i] if i < len(data['revenue']) else None,
                    'net_income': data['net_income'][i] if i < len(data['net_income']) else None,
                    'total_assets': data['total_assets'][i] if i < len(data['total_assets']) else None,
                    'total_liabilities': data['total_liabilities'][i] if i < len(data['total_liabilities']) else None,
                })

    print(f"Data extraction complete for {file_path.stem}. CSV file created at {output_file}")

