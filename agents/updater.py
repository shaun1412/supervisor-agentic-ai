from agents_state import AgentState
from utils.db_utils import update_database
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOllama(model="mistral")

def updater_agent(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content="You are a professional SQL developer. Only output a valid SQL INSERT or UPDATE statement."),
        HumanMessage(content=f"Return ONLY the raw SQL query that answers this request. No explanation, no formatting, no markdown:\n\n{state['query']}")
    ]

    sql_query = llm.invoke(messages).content.strip()
    print(f"\n LLM Generated SQL (Updater):\n{sql_query}\n")

    success = update_database(sql_query)

    return {**state, "update_status": "Success" if success else "Failed"}
