import sqlite3
import pandas as pd

def obtain_header(path) -> str:
    with open(path, "r") as file:
        header = file.readline().strip()
    return header

def obtain_first_line_after_header(path) -> str:
    with open(path, "r") as file:
        lines = file.readlines()
        if len(lines) > 1:
            return lines[1].strip()
        else:
            return None

#create sql file given a path and the code
def create_sql_file(path: str, code: str) -> None:
    with open(path, "w") as file:
        file.write(code)
    print(f"SQL file created at {path}")

#execute sql file given a path
def execute_sql_file(csv_path: str, sql_path: str) -> str:
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
        return "Pass", df
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return "Fail", e
    finally:
        conn.close()