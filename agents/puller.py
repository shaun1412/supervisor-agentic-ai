from agents_state import AgentState
from utils.db_utils import obtain_header
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOllama(model="mistral")

def puller_agent(state: AgentState) -> AgentState:

    #This part can be made into a function, testing for now
    path = state["csv_path"]
    if path is None:
        raise ValueError("CSV path is not provided in the state.")
    header = obtain_header(path)
    if header is None:
        raise ValueError("Failed to obtain header from the CSV file.")
    #^

    messages = [
        SystemMessage(content=f"You are an expert SQL assistant called puller agent. Only output a valid SQL SELECT query. Chat history: {state['messages']}"),
        HumanMessage(content=f"Given the first line of the CSV file: \n\n{header}\n, Only return the raw SQL query that answers this request. No explanation, no formatting, no markdown:\n\n{state['user_query']}\n\n The location of the CSV file is: {path}")
    ]
    
    sql_query = llm.invoke(messages).content.strip()
    print(f"\nLLM Generated SQL (Puller):\n{sql_query}\n")

    return {**state, "sql_query": sql_query, "messages": [{"name": "puller_agent", "content": sql_query}]}