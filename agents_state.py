from typing import TypedDict, Optional

class AgentState(TypedDict):
    query: str
    raw_data: Optional[str]
    processed_data: Optional[str]
    update_status: Optional[str]
