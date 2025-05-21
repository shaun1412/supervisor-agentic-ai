from graph import build_graph
from agents_state import AgentState

if __name__ == "__main__":
    initial_state = AgentState(
        messages=[],
        csv_path="example_data/",
        csv_file="sales_data.csv",
        user_query="For each sales agent, return the total sales amount. The result should be ordered by sales amount in descending order.",
        verification_status=None,
        sql_query=None,
        result=None
    )
    
    graph = build_graph()
    print("User Query:", initial_state["user_query"], "\n")
    result = graph.invoke(initial_state)
    # print("Final Result:", result)
