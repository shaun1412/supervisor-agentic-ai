from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

# --- Agent State Definition ---
class AgentState(TypedDict):
    problem: str
    history: str
    answer: str

# --- Load Ollama Model ---
llm = ChatOllama(model="mistral")

# --- Solver Agent ---
def solve(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content="You are a helpful AI tutor. Solve the problem and explain your steps."),
        HumanMessage(content=f"Problem: {state['problem']}\n\nPrevious Attempts:\n{state['history']}")
    ]
    response = llm(messages).content
    return {
        **state,
        "answer": response
    }

# --- Verifier Agent ---
def verify(state: AgentState):
    answer = state["answer"]
    if "2x+3" in answer.replace(" ", ""):
        print("✅ CORRECT:\n", answer)
        return {"next": END, **state}  # ✅ Still return full state
    else:
        print("❌ WRONG:\n", answer)
        return {"next": "reflect", **state}

# --- Reflector Agent ---
def reflect(state: AgentState) -> AgentState:
    updated_history = state["history"] + f"\nPrevious Attempt:\n{state['answer']}\n"
    return {
        **state,
        "history": updated_history
    }

# --- Build LangGraph ---
workflow = StateGraph(AgentState)
workflow.add_node("solve", solve)
workflow.add_node("verify", verify)
workflow.add_node("reflect", reflect)

workflow.set_entry_point("solve")
workflow.add_edge("solve", "verify")
workflow.add_edge("reflect", "solve")

# Conditional transition based on verifier output
workflow.add_conditional_edges(
    "verify",
    lambda out: out["next"] if isinstance(out, dict) else END,
    {
        "reflect": "reflect",
        END: END
    }
)


graph = workflow.compile()

# --- Run the Agent ---
initial_state = {
    "problem": "What is the derivative of x^2 + 3x + 2?",
    "history": "",
    "answer": ""
}

graph.invoke(initial_state)