import operator
from typing import Annotated, Any, Dict, TypedDict


class AgentState(TypedDict):
    query: str
    results: Annotated[list[Dict[str, Any]], operator.add]
    image_file_path: str
    thread_id: str
