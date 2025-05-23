from agents_state import AgentState
from utils.db_utils import obtain_header, obtain_first_line_after_header
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from agents.llm import llm


def coder_agent(state: AgentState) -> AgentState:

    #This part can be made into a tool call, testing for now
    print(state["csv_path"] + state["csv_file"])

    header = obtain_header(state["csv_path"] + state["csv_file"])
    first_line = obtain_first_line_after_header(state["csv_path"] + state["csv_file"])

    system = SystemMessage(
        content=(
            "You are an expert SQL assistant called coder_agent."
            "Only output a valid SQL SELECT query. No explanation, no formatting, no markdown."
        )
    )

    #obtain the last 3 messages from the history
    history = state["messages"][-2:] if len(state["messages"]) > 2 else state["messages"]

    user = HumanMessage(
        content=(
            f"Given the first line of the table:\n{header}\n"
            f"and the first line of data from the table:\n{first_line}\n"
            "called sales_database.db,\n"
            "Only return the raw SQL query that answers this request:\n"
            f"{state['user_query']}"
        )
    )

    all_messages = [system, *history, user]
    
    ai_response = llm.invoke(all_messages).content.strip() #sql query
    

    print(f"\nLLM Generated SQL (Coder):\n{ai_response}\n")

    return {**state, "sql_query": ai_response, "messages": [user, AIMessage(content=ai_response, name="coder_agent")]}