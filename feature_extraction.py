import os
import re
from pathlib import Path
import json

# Define the input and output directories
input_dir = 'src/data/processed-numeric-contexts'
output_dir = 'src/data/feature'

def extract_features(text):
    """ Extracts financial terms and their contextual data from the text """
    features = {}
    # Define patterns for each feature of interest
    patterns = {
        'revenue': r'\brevenue\b[\s\S]{0,500}',
        'expenses': r'\bexpenses\b[\s\S]{0,500}',
        'net_income': r'\bnet income\b[\s\S]{0,500}',
        'assets': r'\bassets\b[\s\S]{0,500}',
        'liabilities': r'\bliabilities\b[\s\S]{0,500}',
        'equity': r'\bequity\b[\s\S]{0,500}',
        'cash_flow': r'\bcash flow\b[\s\S]{0,500}',
        'operating_margin': r'\boperating margin\b[\s\S]{0,500}',
        'gross_margin': r'\bgross margin\b[\s\S]{0,500}',
        'ebitda': r'\bebitda\b[\s\S]{0,500}',
        'accumulated_depreciation': r'\baccumulated depreciation\b[\s\S]{0,500}',
        'capital_expenditure': r'\bcapital expenditure\b[\s\S]{0,500}',
        'debt': r'\bdebt\b[\s\S]{0,500}',
        'share_repurchase': r'\bshare repurchase\b[\s\S]{0,500}',
        'dividend_payout': r'\bdividend payout\b[\s\S]{0,500}',
        'financial_ratios': r'\b(debt-to-equity ratio|return on equity)\b[\s\S]{0,500}',
        'earnings_per_share': r'\bearnings per share\b[\s\S]{0,500}',
        'tax_rate': r'\btax rate\b[\s\S]{0,500}',
        'segment_revenue': r'\bsegment revenue\b[\s\S]{0,500}',
        'geographic_information': r'\bgeographic\b[\s\S]{0,500}',
        'investment_gains_losses': r'\b(investment gains|investment losses)\b[\s\S]{0,500}',
        'regulatory_changes': r'\bregulatory changes\b[\s\S]{0,500}',
        'legal_issues': r'\blegal issues\b[\s\S]{0,500}',    
        'accrued_liabilities': r'\baccrued liabilities\b[\s\S]{0,500}',
        'common_stock': r'\bcommon stock\b[\s\S]{0,500}',
        'capital_stock': r'\bcapital stock\b[\s\S]{0,500}',
        'subsequent_events': r'\bsubsequent events\b[\s\S]{0,500}',
        'noncurrent_assets': r'\bnoncurrent assets\b[\s\S]{0,500}',
        'fair_value_measurements': r'\bfair value measurements\b[\s\S]{0,500}',
        'level_1_assets': r'\blevel 1 assets\b[\s\S]{0,500}',
        'level_2_assets': r'\blevel 2 assets\b[\s\S]{0,500}',
        'level_3_assets': r'\blevel 3 assets\b[\s\S]{0,500}',
        'debt_securities': r'\bdebt securities\b[\s\S]{0,500}',
        'bank_deposits': r'\bbank deposits\b[\s\S]{0,500}',
        'corporate_debt': r'\bcorporate debt\b[\s\S]{0,500}',
        'government_bonds': r'\bgovernment bonds\b[\s\S]{0,500}',
        'mortgage_backed_securities': r'\bmortgage-backed securities\b[\s\S]{0,500}',
        'asset_backed_securities': r'\basset-backed securities\b[\s\S]{0,500}',
        'hedging_activities': r'\bhedging activities\b[\s\S]{0,500}',
        'foreign_exchange_contracts': r'\bforeign exchange contracts\b[\s\S]{0,500}',
        'designated_hedging': r'\bdesignated hedging\b[\s\S]{0,500}',
        'nondesignated_hedging': r'\bnondesignated hedging\b[\s\S]{0,500}',
        'cash_flow_hedges': r'\bcash flow hedges\b[\s\S]{0,500}',
        'derivative_instruments': r'\bderivative instruments\b[\s\S]{0,500}',
        'geographic_concentration_risk': r'\bgeographic concentration risk\b[\s\S]{0,500}'
    }

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            features[key] = ' '.join(matches)
    return features

def process_files():
    """ Process each file in the directory, extract features, and save them in a structured format """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                features = extract_features(text)

                # Define the output path
                relative_path = os.path.relpath(root, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                os.makedirs(output_path, exist_ok=True)

                output_file_path = os.path.join(output_path, f'{Path(file).stem}_features.json')
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    json.dump(features, f, indent=4)

                print(f'Features extracted and saved for {file}')

if __name__ == '__main__':
    process_files()
