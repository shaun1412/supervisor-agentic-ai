from supervisor import build_graph
from agents_state import AgentState

if __name__ == "__main__":
    initial_state = AgentState(
        messages=[],
        csv_path="example_data/sales_data_small.csv",
        user_query="List out the names of all sales agents with a total transaction amount greater than 1000.",
        verification_status=None,
        sql_query=None,
        result=None
    )
    
    graph = build_graph()
    print("User Query:", initial_state["user_query"], "\n")
    result = graph.invoke(initial_state)
    print("Final Result:", result)
