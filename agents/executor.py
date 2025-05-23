from agents_state import AgentState
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from utils.db_utils import create_sql_file, execute_sql_file
import os
from agents.llm import llm
from utils.db_utils import obtain_header

def executor_agent(state: AgentState) -> AgentState:
    
    #Sometimes the SQL query is not valid, so we need to check if it is valid before running it
    system = SystemMessage(
        content=(
            "Your output will be copied into a file and ran directly. You must output only a valid SQL query"
        )
    )
    history = state["messages"]

    user = HumanMessage(
        content=(
            "Obtain the most recent raw SQL query from the coder agent and run it on the file sales_database.\n"
            "Do not output anything else.\n"
        )
    )
    all_messages = [system, *history, user]
    ai_response = llm.invoke(all_messages).content.strip()

    print(f"\nFinal sql_query:\n{ai_response}\n")

    #change directory to the one where the csv file is located
    os.chdir(state["csv_path"])
    print("(Executor)")
    create_sql_file("query.sql", ai_response)
    result = execute_sql_file(state["csv_file"], "query.sql") #returns [verification_status, result]
    os.chdir("..")



    if result[0] == "Fail":
        header = obtain_header(state["csv_path"] + state["csv_file"])
        system = SystemMessage(
            content=(
                "You are a professional summarizer called executor_agent."
                "Briefly summarize the the error message from running the SQL and provide suggestions on fixing it."
            )
        )
        history = state["messages"]
        user = HumanMessage(
            content=(
                f"Summarize the error message given the following SQL query:\n{ai_response}\n"
                f"Error message:\n{result[1]}\n"
                f"Header of the file:\n{header}\n"
                f"called sales_database, from a sqlite3 database\n"
            )
        )

        all_messages = [system, *history, user]
        ai_response = llm.invoke(all_messages).content.strip()
        print(f"\nSummary of the error message (Executor):\n{ai_response}\n")
        
    print(f"\nResult of the SQL query:\n{result}\n")

    return {**state, "messages": [user, AIMessage(content=ai_response, name="executor_agent")], "verification_status": result[0]}
