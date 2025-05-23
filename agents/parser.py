from agents_state import AgentState
from utils.db_utils import obtain_header, obtain_first_line_after_header
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from agents.llm import llm


def parser_agent(state: AgentState) -> AgentState:

    if state["user_query"] is None:
        # state["user_query"] = "List in descending order the total sales by each agent for the month of January and February 2025"
        state["user_query"] = "Which salesperson had the greatest total sales"
    else:
        state["user_query"] = input("Please provide a user query: ")
    
    print("User Query:", state["user_query"], "\n")

    header = obtain_header(state["csv_path"] + state["csv_file"])
    first_line = obtain_first_line_after_header(state["csv_path"] + state["csv_file"])
    print(f"\nHeader of the CSV file:\n{header}\n")
    print(f"First line of the CSV file:\n{first_line}\n")
    if header is None or first_line is None:
        raise ValueError("Failed to obtaining data from csv file")
    #^

    system = SystemMessage(
        content=(
            "You are a parser agent called parser_agent. Your first word must either be Pass or Fail."
            "Your task is to determine if it is possible to create a SQL query to answer the user query given the header and first line of the table."
            "If it cannot, return Fail followed by an explanation. Otherwise return Pass and then reword the user query in the clearest way possible."
            "If it is Pass, do not provide anything else other than the reworded query after. Do not provide SQL code, just the reworded query."
        )
    )

    user = HumanMessage(
        content=(
            f"Given the header line of the table:\n{header}\n and the first line of the table:\n{first_line}\n."
            "The first line of the table is to show the formatting of the data. There are many more lines\n"
            f"Explain if the user query: \n{state['user_query']}\n can be converted into a SQL query.\n"
        )
    )

    all_messages = [system, user]
    
    ai_response = llm.invoke(all_messages).content.strip()
    print(f"\nParsing validity of user querty (Parser):\n{ai_response}\n")

    verification_status = ai_response.split()[0].strip()[0:4]
    if verification_status not in ["Pass", "Fail"]:
        raise ValueError(f"Unexpected verification status: {verification_status}")
    
    return {**state, "sql_query": ai_response[4:], "verification_status": verification_status}