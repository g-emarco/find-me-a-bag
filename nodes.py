from enum import Enum
from typing import Any, Dict

from state import AgentState

HYBRID_SEARCH = "hybrid_search"
KEYWORD_SEARCH = "keyword_search"
SEMANTIC_SEARCH = "semantic_search"


class Searches(Enum):
    HYBRID_SEARCH = "HYBRID_SEARCH"
    KEYWORD_SEARCH = "KEYWORD_SEARCH"
    SEMANTIC_SEARCH = "SEMANTIC_SEARCH"


def hybrid_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    print(f"hybrid_search enter, {query=}")
    return {}


def keyword_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    print(f"keyword_search enter, {query=}")
    return {}


def semantic_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    print(f"semantic_search enter, {query=}")

    return {}
