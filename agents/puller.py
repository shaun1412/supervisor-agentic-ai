from agents_state import AgentState
from utils.db_utils import run_sql_query
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOllama(model="mistral")

def puller_agent(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content="You are an expert SQL assistant. Only output a valid SQL SELECT query."),
        HumanMessage(content=f"Convert this user query to SQL:\n\n{state['query']}")
    ]
    
    sql_query = llm.invoke(messages).content.strip()
    print(f"\n LLM Generated SQL (Puller):\n{sql_query}\n")

    result = run_sql_query(sql_query)
    return {**state, "raw_data": result}
