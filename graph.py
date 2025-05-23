from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableLambda
from agents_state import AgentState
from agents.parser import parser_agent
from agents.coder import coder_agent
from agents.verifier import verifier_agent
from agents.executor import executor_agent


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("parser", RunnableLambda(parser_agent))
    graph.add_node("coder", RunnableLambda(coder_agent))
    graph.add_node("verifier", RunnableLambda(verifier_agent))
    graph.add_node("executor", RunnableLambda(executor_agent))

    graph.add_edge(START, "parser")
    graph.add_conditional_edges(
        "parser",
        get_verification_status,
        {
            "Pass": "coder",
            "Fail": "parser",
        },
    )
    graph.add_edge("coder", "executor")
    # graph.add_conditional_edges(
    #     "verifier",
    #     get_verification_status,
    #     {
    #         "Pass": "executor",
    #         "Fail": "coder",
    #     },
    # )
    graph.add_conditional_edges(
        "executor",
        get_verification_status,
        {
            "Pass": END,
            "Fail": "coder",
        },
    )

    return graph.compile()

def get_verification_status(state):
    return state["verification_status"]