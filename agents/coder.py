from agents_state import AgentState
from utils.db_utils import obtain_header
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3")

def coder_agent(state: AgentState) -> AgentState:

    #This part can be made into a tool call, testing for now
    print(state["csv_path"] + state["csv_file"])

    header = obtain_header(state["csv_path"] + state["csv_file"])
    print(f"\nHeader of the CSV file:\n{header}\n")
    if header is None:
        raise ValueError("Failed to obtain header from the CSV file.")
    #^

    messages = [
        SystemMessage(content=f"You are an expert SQL assistant called coder agent. Only output a valid SQL SELECT query. No explanation, no formatting, no markdown. Chat history: {state['messages'][-1] if state['messages'] else ''}"),
        HumanMessage(content=f"Given the first line of the table: \n{header}\n called sales_database,\n Only return the raw SQL query that answers this request: \n{state['user_query']}\n.")
    ]
    
    
    sql_query = llm.invoke(messages).content.strip()
    


    print(f"\nLLM Generated SQL (Coder):\n{sql_query}\n")

    return {**state, "sql_query": sql_query, "messages": [{"name": "coder_agent", "content": sql_query}]}