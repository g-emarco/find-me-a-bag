from agent.main import router
from agent.nodes import Searches
from agent.state import AgentState


def test_router_semantic() -> None:
    query = "find me a bag similar to this bag"
    state: AgentState = AgentState(query=query)
    res = router(state)
    assert res == Searches.SEMANTIC_SEARCH.value


def test_router_keyword() -> None:
    query = "find me a a black bag"
    state: AgentState = AgentState(query=query)
    res = router(state)
    assert res == Searches.KEYWORD_SEARCH.value


def test_router_hybrid() -> None:
    query = "find me a a black bag similar to my bag"
    state: AgentState = AgentState(query=query)
    res = router(state)
    assert res == Searches.HYBRID_SEARCH.value
