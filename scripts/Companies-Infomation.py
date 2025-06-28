import pandas as pd
from sqlalchemy import create_engine, text

# Load the NIFTY50 data from NSE
url = "https://archives.nseindia.com/content/indices/ind_nifty50list.csv"
df = pd.read_csv(url)

# Clean and prepare the data
df.drop(columns=['Series', 'ISIN Code'], inplace=True)
df = df[['Symbol', 'Company Name', 'Industry']]
df['Symbol'] = df['Symbol'].astype(str) + ".NS"
df.rename(columns={"Symbol": "Ticker", "Industry": "Sector"}, inplace=True)

# Save the cleaned data to a CSV file
output_file = "./data/nifty50_current_companies_info.csv"
df.to_csv(output_file, index=False)
print(f"NIFTY50 companies information saved to {output_file} successfully!")

