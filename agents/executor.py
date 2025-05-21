from agents_state import AgentState
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from utils.db_utils import create_sql_file, execute_sql_file
import os

llm = ChatOllama(model="llama3")

def executor_agent(state: AgentState) -> AgentState:

    #Sometimes the SQL query is not valid, so we need to check if it is valid before running it
    messages = [
        SystemMessage(content="Your output will be copied into a a file and ran directly. You must output only a valid SQL query"),
        HumanMessage(content=f"obtain the raw SQL query from: \n{state['sql_query']}. \n Do not output anything else.")
    ]

    sql_query = llm.invoke(messages).content.strip()
    print(f"\nFinal sql_query:\n{sql_query}\n")

    #change directory to the one where the csv file is located
    os.chdir(state["csv_path"])
    print("(Executor)")
    create_sql_file("query.sql", sql_query)
    result = execute_sql_file(state["csv_file"], "query.sql")

    os.chdir("..")


    print(f"\nResult of the SQL query:\n{result}\n")

    return {**state, "messages": [{"name": "executor_agent", "content": result}]}
