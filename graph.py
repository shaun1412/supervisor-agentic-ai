from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableLambda
from agents_state import AgentState
from agents.coder import coder_agent
from agents.verifier import verifier_agent
from agents.executor import executor_agent


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("coder", RunnableLambda(coder_agent))
    graph.add_node("verifier", RunnableLambda(verifier_agent))
    graph.add_node("executor", RunnableLambda(executor_agent))

    graph.add_edge(START, "coder")
    graph.add_edge("coder", "verifier")
    graph.add_conditional_edges(
        "verifier",
        get_verification_status,
        {
            "Pass": "executor",
            "Fail": "coder",
        },
    )
    graph.add_edge("executor", END)
    return graph.compile()

def get_verification_status(state):
    return state["verification_status"]