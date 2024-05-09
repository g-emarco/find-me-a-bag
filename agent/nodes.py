from enum import Enum
from typing import Any, Dict

from langchain_google_vertexai import VertexAIEmbeddings
from agent.state import AgentState

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
    return {"result": "aaa"}


def keyword_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"]

    sparse_embedding = ""
    print(f"keyword_search enter, {query=}")
    return {
        "results": [
            {
                "id": 2,
                "bucket_uri": "https://storage.googleapis.com/public_bags/black%20channel-like%201.png",
                "name": "Black Channel Bag",
                "description": "A durable canvas backpack for everyday use. Fun and beautiful at the same time",
            }
        ]
    }


def semantic_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    print(f"semantic_search enter, {query=}")
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")
    embedding = embeddings.embed_query(text=query)
    return {}
