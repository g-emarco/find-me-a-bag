import operator
from typing import Annotated, Any, Dict, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AssistantAgentState(TypedDict):
    bag_id: str
    messages: Annotated[list[AnyMessage], add_messages]
    user_id: str
    user_data: str
    query: str
