import sqlite3
import pandas as pd
import os
# os.chdir('example_data')

csv_path = 'sales_data.csv'
sql_path = 'query.sql'


# Connect to the SQLite database (or create it if it doesn't exist)
df = pd.read_csv(csv_path)
conn = sqlite3.connect('sales_database.db')  # Use an in-memory database for testing
df.to_sql('sales_database', conn, if_exists='replace', index=False)

# Read the SQL file
with open(sql_path, 'r') as file:
    sql_script = file.read()

# Execute the SQL script
try:
    df = pd.read_sql_query(sql_script, conn)
    print("SQL query executed successfully.")
    print(df)
except Exception as e:
    print(f"Error executing SQL query: {e}")
    print(None)
finally:
    conn.close()

os.chdir("..")