import operator
from typing import TypedDict, Annotated, Any, Dict


class AgentState(TypedDict):
    query: str
    results: Annotated[list[Dict[str, Any]], operator.add]
