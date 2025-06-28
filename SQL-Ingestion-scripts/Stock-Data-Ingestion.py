import pandas as pd
from sqlalchemy import create_engine, text
import os

# Load the CSV
file_path = os.path.join("..", "data", "enhanced_stock_data.csv")
df = pd.read_csv(file_path)

# MySQL credentials
user = "root"
password = "7742"
host = "localhost"
port = 3306
database = "nifty50_stock_data"

# Create SQLAlchemy engine
connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# Drop and create table
drop_sql = "DROP TABLE IF EXISTS StockFeatures;"
create_sql = """
CREATE TABLE IF NOT EXISTS StockFeatures (
    Date DATE,
    Ticker VARCHAR(20),
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume BIGINT,
    `Daily_Return_%` FLOAT,
    MA_7 FLOAT,
    MA_30 FLOAT,
    Volatility_30 FLOAT
);
"""

with engine.connect() as connection:
    connection.execute(text(drop_sql))
    connection.execute(text(create_sql))
    print("✅ Table created or reset: StockFeatures")

# Upload CSV data into MySQL
print(f"📦 Uploading {len(df)} rows...")
df.to_sql(name='StockFeatures', con=engine, if_exists='append', index=False)
print("✅ Data successfully inserted into MySQL.")
