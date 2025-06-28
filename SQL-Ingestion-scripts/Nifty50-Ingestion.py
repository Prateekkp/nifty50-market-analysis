import pandas as pd
from sqlalchemy import create_engine, text
import os

# Load the CSV
file_path = os.path.join("..", "data", "nifty50_data.csv")
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

# Step 4: Drop and create table
drop_sql = "DROP TABLE IF EXISTS nifty50_index;"
create_sql = """
CREATE TABLE IF NOT EXISTS nifty50_index (
    Date DATE,
    Ticker VARCHAR(20),
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume BIGINT
);
"""

with engine.connect() as connection:
    connection.execute(text(drop_sql))
    connection.execute(text(create_sql))
    print("Table 'nifty50_index' has been dropped and recreated.")

# Upload CSV data into MySQL
print(f"Uploading {len(df)} rows...")
df.to_sql(name='nifty50_index', con=engine, if_exists='append', index=False)
print("Data successfully inserted into MySQL.")
