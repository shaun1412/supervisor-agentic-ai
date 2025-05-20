from agents_state import AgentState
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3")

def verifier_agent(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content="You are a professional SQL code verifier. The first word you return must either be Pass or Fail."),
        HumanMessage(content=f"Verify the following SQL query \n\n{state['sql_query']}\n\n can be executed on the file located at \n\n{state['csv_path']}\n\nand satisfies the following request:\n\n{state['user_query']}\n\n If it does, return Pass. If it doesn't, return Fail. \n\n Afterwards, give a brief explanation of why it passes or fails.")
    ]

    verification = llm.invoke(messages).content.strip()
    print(f"\nVerification of the sql query (Verifier):\n{verification}\n")

    verification_status = verification.split()[0].strip()[0:4]
    if verification_status not in ["Pass", "Fail"]:
        raise ValueError(f"Unexpected verification status: {verification_status}")
    
    explanation = " ".join(verification.split()[1:])

    return {**state, "verification_status": verification_status, "messages": [{"name": "verifier_agent", "content": verification}]}
