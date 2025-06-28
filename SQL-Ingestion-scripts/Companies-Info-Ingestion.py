import pandas as pd
from sqlalchemy import create_engine, text
import os

# Load the CSV
file_path = os.path.join("..", "data", "nifty50_current_companies_info.csv")
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
drop_sql = "DROP TABLE IF EXISTS Companies_Information;"
create_sql = """
CREATE TABLE companies_information (
    Ticker VARCHAR(20) PRIMARY KEY,
    `Company Name` VARCHAR(255),
    Sector VARCHAR(100)
);
"""

with engine.connect() as connection:
    connection.execute(text(drop_sql))
    connection.execute(text(create_sql))
    print("Table 'nifty50_index' has been dropped and recreated.")

# Upload CSV data into MySQL
df.to_sql(name='companies_information', con=engine, if_exists='append', index=False)
print("Data saved to MySQL table 'companies_information' successfully!")
