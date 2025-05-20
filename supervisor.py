from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from typing import TypedDict
from agents_state import AgentState
from agents.puller import puller_agent
from agents.processor import processor_agent
from agents.updater import updater_agent




def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("puller", RunnableLambda(puller_agent))
    graph.add_node("processor", RunnableLambda(processor_agent))
    graph.add_node("updater", RunnableLambda(updater_agent))

    graph.set_entry_point("puller")
    graph.add_edge("puller", "processor")
    graph.add_edge("processor", "updater")
    graph.add_edge("updater", END)

    return graph.compile()
