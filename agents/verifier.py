from agents_state import AgentState
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from utils.db_utils import obtain_header

llm = ChatOllama(model="llama3")

def verifier_agent(state: AgentState) -> AgentState:

    header = obtain_header(state["csv_path"] + state["csv_file"]) 
    messages = [
        SystemMessage(content="You are a professional SQL code verifier. The first word you return must either be Pass or Fail."),
        HumanMessage(content=f"Verify the following SQL query: \n{state['sql_query']}\n can be executed on the file: \nsales_database\n given the following header \n{header}\nand satisfies the following request:\n\n{state['user_query']}\n\n If it does and there are no issues, return Pass. If it doesn't, return Fail. \n\n Ensure the syntax is correct too. Afterwards, give a brief explanation of why it passes or fails.")
    ]

    verification = llm.invoke(messages).content.strip()
    print(f"\nVerification of the sql query (Verifier):\n{verification}\n")

    verification_status = verification.split()[0].strip()[0:4]
    if verification_status not in ["Pass", "Fail"]:
        raise ValueError(f"Unexpected verification status: {verification_status}")

    return {**state, "verification_status": verification_status, "messages": [{"name": "verifier_agent", "content": verification}]}
