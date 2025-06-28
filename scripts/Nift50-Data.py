import pandas as pd
import yfinance as yf
from datetime import datetime

# Date Range
start_date = "2020-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

# Download NIFTY 50 Index
df = yf.download("^NSEI", start=start_date, end=end_date)

# Flatten multi-index columns if needed
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Prepare final DataFrame
df.reset_index(inplace=True)
# Convert to yyyy-mm-dd string for MySQL
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d') 
df['Ticker'] = "^NSEI"
df = df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Save to CSV
df.to_csv("./data/nifty50_data.csv", index=False)
print("NIFTY 50 data saved to nifty50_data.csv")
