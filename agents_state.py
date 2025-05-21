from typing import TypedDict, Optional, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add] #.add > Reducer to appended to the existing list in the state
    csv_path: Optional[str]
    csv_file: Optional[str]
    user_query: str
    sql_query: Optional[str]
    verification_status: Optional[str]
    result: Optional[str]

