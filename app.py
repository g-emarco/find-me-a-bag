import base64
import datetime
import json
from typing import Dict, List

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from flask import Flask, abort, jsonify, render_template, request
from google.cloud.firestore_v1 import FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_firestore import FirestoreChatMessageHistory

from agent.main import compiled_graph
from assistant_agent.graph import graph
from db_setup import db

load_dotenv()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_bag_by_text_query(text_query: str, thread_id: str):
    return compiled_graph.invoke({"query": text_query, "thread_id": thread_id})


def get_bag_by_image(image_file_path: str, thread_id: str):
    return compiled_graph.invoke(
        {"query": "", "image_file_path": image_file_path, "thread_id": thread_id}
    )


def get_bag_by_image_and_text_query(
    text_query: str, image_file_path: str, thread_id: str
):
    return compiled_graph.invoke(
        {
            "query": text_query,
            "image_file_path": image_file_path,
            "thread_id": thread_id,
        }
    )


# @app.route("/bags", methods=["POST", "GET"])
# def get_bags():
#     graph_res = {}
#     if request.method == "POST":
#
#         if not request.json:
#             abort(400)
#
#         query = request.json.get("query")
#         im_b64 = request.json.get("image")
#         thread_id = request.json.get("thread_id", "default-thread-id12312312")
#
#         print(f"***********************************")
#
#         if im_b64:
#             img_bytes = base64.b64decode(im_b64.encode("utf-8"))
#             print(f"{img_bytes[:50]=}")
#
#             with open("tmp_image.jpeg", "wb") as file:
#                 file.write(img_bytes)
#             if not query:
#                 graph_res = get_bag_by_image(
#                     image_file_path="tmp_image.jpeg", thread_id=thread_id
#                 )
#
#         if im_b64 and query:
#             graph_res = get_bag_by_image_and_text_query(
#                 text_query=query, image_file_path="tmp_image.jpeg", thread_id=thread_id
#             )
#
#         if query and not im_b64:
#             graph_res = get_bag_by_text_query(text_query=query, thread_id=thread_id)
#
#         documents = (
#             db.collection("Bags")
#             .where(filter=FieldFilter("id", "in", graph_res["results"]))
#             .get()
#         )
#         documents = [d.to_dict() for d in documents]
#
#     if request.method == "GET":
#         query = request.args.get("query")
#         thread_id = request.args.get("thread_id", "default-thread-id12312312")
#
#         if query:
#             print("filtering bags...")
#             graph_res = get_bag_by_text_query(text_query=query, thread_id=thread_id)
#             documents = (
#                 db.collection("Bags")
#                 .where(filter=FieldFilter("id", "in", graph_res["results"]))
#                 .get()
#             )
#             documents = [d.to_dict() for d in documents]
#
#         else:
#             print("fetching all bags...")
#             documents = get_all_documents_from_firestore2()
#
#     filtered_bags = documents
#     response_dict = {
#         "bags": filtered_bags,
#         "action": graph_res["action"] if graph_res.get("action") else "no_search",
#     }
#     return jsonify(response_dict)

@app.route("/bags", methods=["POST", "GET"])
def get_bags2():
    graph_res = {}
    if request.method == "POST":

        if not request.json:
            abort(400)

        query = request.json.get("query")
        im_b64 = request.json.get("image")
        thread_id = request.json.get("thread_id", "default-thread-id12312312")

        print(f"***********************************")

        if im_b64:
            img_bytes = base64.b64decode(im_b64.encode("utf-8"))
            print(f"{img_bytes[:50]=}")

            with open("tmp_image.jpeg", "wb") as file:
                file.write(img_bytes)
            if not query:
                graph_res = get_bag_by_image(
                    image_file_path="tmp_image.jpeg", thread_id=thread_id
                )

        if im_b64 and query:
            graph_res = get_bag_by_image_and_text_query(
                text_query=query, image_file_path="tmp_image.jpeg", thread_id=thread_id
            )

        if query and not im_b64:
            graph_res = get_bag_by_text_query(text_query=query, thread_id=thread_id)

        documents = (
            db.collection("Profiles")
            .where(FieldPath.document_id(), "in", graph_res["results"])
            .get()
        )
        documents = [d.to_dict() for d in documents]
        for d in documents:
            d.pop('embedding_field')

    if request.method == "GET":
        query = request.args.get("query")
        thread_id = request.args.get("thread_id", "default-thread-id12312312")

        if query:
            print("filtering bags...")
            graph_res = get_bag_by_text_query(text_query=query, thread_id=thread_id)
            documents = (
                db.collection("Profiles")
                .where(FieldPath.document_id(), "in", graph_res["results"])
                .get()
            )
            documents = [d.to_dict() for d in documents]
            for d in documents:
                d.pop('embedding_field')
        else:
            print("fetching all bags...")
            documents = get_all_documents_from_firestore2()

    filtered_bags = documents
    response_dict = {
        "bags": filtered_bags,
        "action": graph_res["action"] if graph_res.get("action") else "no_search",
    }
    return jsonify(response_dict)

def get_all_documents_from_firestore() -> List[Dict[str, str]]:

    data = db.collection("Bags").stream()
    documents = [d.to_dict() for d in data]

    return documents

def get_all_documents_from_firestore2() -> List[Dict[str, str]]:

    data = db.collection("Profiles").stream()
    documents = [d.to_dict() for d in data]
    documents = [d for d in documents if 'country' in d]

    for doc in documents:
        if "embedding_field" in doc:
            doc.pop("embedding_field")
        print(doc)

        doc['price'] = doc['country']



    return documents

@app.route("/assistant", methods=["GET"])
def assistant():
    query = request.args.get("query")
    thread_id = request.args.get("thread_id")
    chat_history = FirestoreChatMessageHistory(session_id=thread_id)

    res = graph.invoke(
        {
            "messages": [HumanMessage(content=query)],
            "user_id": "emKszv8xjISy446FJNmK",
            "query": query,
        }
    )
    chat_history.add_message(HumanMessage(content=query))
    chat_history.add_message(res["messages"][-1])

    print("**********")
    print(res)
    history = [
        {
            "role": (type(message).__name__),
            "content": message.content,
            "time": datetime.datetime.now().strftime("%H:%M"),
        }
        for message in chat_history.messages
        if message.content and type(message).__name__ != "ToolMessage"
    ]
    return {"messages": [history[-1]]}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8080)
