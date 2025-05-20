from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from typing import TypedDict
from agents_state import AgentState
from agents.puller import puller_agent
from agents.verifier import verifier_agent


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("puller", RunnableLambda(puller_agent))
    graph.add_node("verifier", RunnableLambda(verifier_agent))

    graph.add_edge(START, "puller")
    graph.add_edge("puller", "verifier")
    graph.add_conditional_edges(
        "verifier",
        get_verification_status,
        {
            "Pass": END,
            "Fail": "puller",
        },

    )

    return graph.compile()

def get_verification_status(state):
    return state["verification_status"]