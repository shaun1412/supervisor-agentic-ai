from graph import build_graph
from agents_state import AgentState

if __name__ == "__main__":
    initial_state = AgentState(
        messages=[],
        csv_path="example_data/",
        csv_file="sales_data.csv",
        user_query=None,
        verification_status=None,
        sql_query=None,
        result=None
    )
    
    graph = build_graph()
    result = graph.invoke(initial_state)
    # print("Final Result:", result)