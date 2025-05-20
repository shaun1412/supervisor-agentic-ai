def run_sql_query(query: str) -> str:
    print(f"Running query: {query}")
    return "id:1,name:Alice\nid:2,name:Bob"  # Mocked data

def update_database(query: str) -> bool:
    print(f"Updating database with:\n{query}")
    return True  # Always succeeds for now
