import json
import os
import subprocess
from enum import Enum
from typing import Any, Dict

import requests
from langchain_google_vertexai import VertexAIEmbeddings

from agent.state import AgentState
from corpus import bm25

VECTORDB_PROJECT_ID = "<my_project_id>"
VECTORDB_REGION = "me-west1"
VECTORDB_BUCKET = "<my_gcs_bucket>"
VECTORDB_BUCKET_URI = f"gs://{VECTORDB_BUCKET}"

MAX_RES = 10


class Searches(Enum):
    HYBRID_SEARCH = "HYBRID_SEARCH"
    KEYWORD_SEARCH = "KEYWORD_SEARCH"
    SEMANTIC_SEARCH = "SEMANTIC_SEARCH"


def hybrid_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"].strip("'")
    print(f"hybrid_search enter, {query=}")

    return matching_engine_search(query=query, hybrid=True)


def keyword_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"].strip("'")

    return matching_engine_search(query=query)


def matching_engine_search(query: str, hybrid: bool = False) -> Dict[str, Any]:
    print(f"matching_engine_search enter, {query=}, {hybrid=}")

    sparse_vector = bm25.encode_documents(query)
    embeddings = VertexAIEmbeddings(model_name="multimodalembedding@001")
    dense_embedding = embeddings.embed_query(text=query)

    text_query_sparse_embedding_modified = (
        str(sparse_vector).replace("'", '"').replace("indices", "dimensions")
    )
    print("###################################")

    url = "https://1545454881.me-west1-984298407984.vdb.vertexai.goog/v1/projects/984298407984/locations/me-west1/indexEndpoints/6212715685957599232:findNeighbors"

    if os.environ.get("LOCAL"):
        access_token_command = "gcloud auth print-access-token"
        access_token_result = subprocess.run(
            access_token_command, shell=True, capture_output=True, text=True
        )
        access_token = access_token_result.stdout.strip()
    else:
        import google.auth
        import google.auth.transport.requests

        creds, project = google.auth.default()

        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        access_token = creds.token

    data = {
        "deployedIndexId": "index_demo_summit_deployed",
        "queries": [
            {
                "datapoint": {
                    "sparseEmbedding": json.loads(text_query_sparse_embedding_modified),
                    "featureVector": dense_embedding,
                },
                "neighborCount": 10,
                "rrf": {"alpha": 0.501 if hybrid else 0},
            }
        ],
        "returnFullDatapoint": False,
    }

    if not hybrid:
        data['queries'][0]['datapoint'].pop("featureVector")
    if hybrid:
        data['queries'][0]['neighborCount'] = 2


    response = requests.post(
        url, headers={"Authorization": f"Bearer {access_token}"}, json=data
    )
    response_content = json.loads(response.content)
    print(response.status_code)
    print(response_content)

    ids = [
        neighbor["datapoint"]["datapointId"]
        for neighbor in response_content["nearestNeighbors"][0]["neighbors"]
    ]

    print(f"{ids=}")
    return {"results": ids[:MAX_RES]}


def semantic_search(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    print(f"************semantic_search enter ************")
    print(f"************{state=}******")

    embeddings = VertexAIEmbeddings(model_name="multimodalembedding@001")

    if image_file_path := state.get("image_file_path"):
        print(f"embedding {image_file_path=}")
        embedding = embeddings.embed_image(image_path=image_file_path)
    if query:
        embedding = embeddings.embed_query(text=query)

    from google.cloud import aiplatform_v1

    API_ENDPOINT = "1545454881.me-west1-984298407984.vdb.vertexai.goog"
    INDEX_ENDPOINT = (
        "projects/984298407984/locations/me-west1/indexEndpoints/6212715685957599232"
    )
    DEPLOYED_INDEX_ID = "index_demo_summit_deployed"

    client_options = {"api_endpoint": API_ENDPOINT}
    vector_search_client = aiplatform_v1.MatchServiceClient(
        client_options=client_options,
    )

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
    ids = [
        neighbor.datapoint.datapoint_id
        for neighbor in response.nearest_neighbors[0].neighbors.pb
    ]
    print(f"neighbors are {ids=}")
    return {"results": ids[:MAX_RES]}
