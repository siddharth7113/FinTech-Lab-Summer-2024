import logging
from sec_edgar_downloader import Downloader
import os
 

#Configure Logging
logging.basicConfig(level=logging.INFO, filename='downloader.log', filemode = 'w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

#Logging into Console as well
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


#Download directory for Data,Company Name and Email
download_dir = 'src/data'
company_name = "MyCompanyName"
email_address = "my.email1@domain.com"


#Ensure the  directory exsist
os.makedirs(download_dir, exist_ok=True)

# Initialize a downloader instance with company name and email
dl = Downloader(company_name, email_address, download_dir)

# Company tickers
companies = ['AAPL', 'MSFT', 'DELL',] 
start_year = 1995
end_year = 2023

for ticker in companies:
    try:
        expected_years = list(range(start_year, end_year + 1))
        downloaded_years = []

        for year in expected_years:
            #Download filings year by year to check each year individually
            num_downloaded = dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year+1}-01-01")
            if num_downloaded > 0:
                downloaded_years.append(year)
        
        missing_years = [year for year in expected_years if year not in downloaded_years]
        logging.info(f"Downloaded {len(downloaded_years)} 10-K filings for {ticker} from {start_year} to {end_year}.")

        if missing_years:
            logging.warning(f"Missing filings for {ticker} for years: {missing_years}")
        else:
            logging.info(f"All expected filings for {ticker} have been downloaded.")

    except Exception as e:
        logging.error(f"Failed to download filings for {ticker}: {e}")
