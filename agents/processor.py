from agents_state import AgentState

def processor_agent(state: AgentState) -> AgentState:
    raw = state["raw_data"]
    lines = raw.strip().split("\n")

    structured = []
    for line in lines:
        fields = line.split(",")
        formatted = {kv.split(":")[0].strip(): kv.split(":")[1].strip() for kv in fields}
        structured.append(formatted)

    # Convert to a pseudo-table string like: "users,id:1,name:Alice;id:2,name:Bob"
    flat = ";".join([",".join([f"{k}:{v}" for k, v in row.items()]) for row in structured])
    cleaned_data = f"users,{flat}"

    return {**state, "processed_data": cleaned_data}
