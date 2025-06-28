import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Folder setup
os.makedirs("stock_data", exist_ok=True)

# Get NIFTY 50 tickers
nifty_url = "https://archives.nseindia.com/content/indices/ind_nifty50list.csv"
nifty_df = pd.read_csv(nifty_url)
tickers = (nifty_df['Symbol'] + ".NS").tolist()

# Date range
start_date = "2020-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

# Download individual stock data
for ticker in tickers:
    file_path = f"stock_data/data_{ticker}.csv"
    if os.path.exists(file_path):
        print(f"⏩ Skipping: {ticker}")
        continue

    print(f"📦 Downloading: {ticker}")
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty or df.isnull().all().any():
        print(f"⚠️ Skipping {ticker} due to missing data.")
        continue

    df.reset_index(inplace=True)
    df['Ticker'] = ticker
    df = df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df.to_csv(file_path, index=False)
    print(f"✅ Saved: {file_path}")

# Merge all stock CSVs
print("\n🔗 Merging all CSVs...")
merged_df = pd.DataFrame()

for ticker in tickers:
    file_path = f"stock_data/data_{ticker}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, header=0)
        merged_df = pd.concat([merged_df, df], axis=0)

# Clean data
merged_df = merged_df[pd.to_datetime(merged_df['Date'], errors='coerce').notnull()]
merged_df = merged_df[pd.to_numeric(merged_df['Open'], errors='coerce').notnull()]
merged_df = merged_df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
merged_df.to_csv("merged_stock_data.csv", index=False)
print("📦 Saved cleaned merged data as 'merged_stock_data.csv'")

# Feature Engineering
print("\n⚙️ Performing feature engineering...")

df = merged_df.copy()
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date', 'Ticker'], inplace=True)

# Convert numeric columns (in case of comma issues)
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

# Sort data
df.sort_values(by=['Ticker', 'Date'], inplace=True)

# Feature Engineering: per ticker
# % Daily Return
df['Daily_Return_%'] = df.groupby('Ticker')['Close'].pct_change() * 100

# Moving Averages
df['MA_7'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=7).mean())
df['MA_30'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=30).mean())

# FIXED: Volatility = std dev of % return
df['Volatility_30'] = df.groupby('Ticker')['Daily_Return_%'].transform(lambda x: x.rolling(window=30).std())


# Drop rows with NaNs due to rolling
df.dropna(inplace=True)

# Save final file
df.to_csv("./data/enhanced_stock_data.csv", index=False)
print("✅ Feature engineering complete. File saved: enhanced_stock_data.csv")
