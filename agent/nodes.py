import json
import subprocess
from enum import Enum
from typing import Any, Dict

from langchain_google_vertexai import VertexAIEmbeddings, VectorSearchVectorStore
from agent.state import AgentState
import requests

VECTORDB_PROJECT_ID = "<my_project_id>"
VECTORDB_REGION = "me-west1"
VECTORDB_BUCKET = "<my_gcs_bucket>"
VECTORDB_BUCKET_URI = f"gs://{VECTORDB_BUCKET}"


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
    embeddings = VertexAIEmbeddings(model_name="multimodalembedding@001")
    embedding = embeddings.embed_query(text=query)

    from google.cloud import aiplatform_v1

    # Set variables for the current deployed index.
    API_ENDPOINT = "1545454881.me-west1-984298407984.vdb.vertexai.goog"
    INDEX_ENDPOINT = (
        "projects/984298407984/locations/me-west1/indexEndpoints/6212715685957599232"
    )
    DEPLOYED_INDEX_ID = "index_demo_summit_deployed"

    client_options = {"api_endpoint": API_ENDPOINT}
    vector_search_client = aiplatform_v1.MatchServiceClient(
        client_options=client_options,
    )

    # Build FindNeighborsRequest object
    datapoint = aiplatform_v1.IndexDatapoint(feature_vector=embedding)
    query = aiplatform_v1.FindNeighborsRequest.Query(
        datapoint=datapoint, neighbor_count=10
    )
    request = aiplatform_v1.FindNeighborsRequest(
        index_endpoint=INDEX_ENDPOINT,
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query],
        return_full_datapoint=False,
    )

    response = vector_search_client.find_neighbors(request)

    print(response)
