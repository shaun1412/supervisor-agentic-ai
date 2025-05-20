from supervisor import build_graph
from agents_state import AgentState

if __name__ == "__main__":
    initial_state = AgentState(
        query="SELECT * FROM users",
        raw_data=None,
        processed_data=None,
        update_status=None
    )
    
    graph = build_graph()
    result = graph.invoke(initial_state)
    print("Final Result:", result)
