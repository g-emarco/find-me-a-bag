import base64
from typing import List, Dict

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, render_template, request, abort
from google.cloud.firestore_v1 import FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath

from agent.main import compiled_graph

load_dotenv()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_bag_by_text_query(text_query: str):
    return compiled_graph.invoke({"query": text_query})


def get_bag_by_image(image_file_path: str):
    return compiled_graph.invoke({"query": "", "image_file_path": image_file_path})


def get_bag_by_image_and_text_query(text_query:str,image_file_path:str):
    return compiled_graph.invoke({"query": text_query, "image_file_path": image_file_path})


@app.route("/bags", methods=["POST", "GET"])
def get_bags():
    if request.method == "POST":

        if not request.json or "image" not in request.json:
            abort(400)

        query = request.json.get("query")
        im_b64 = request.json.get("image")

        if im_b64:
            img_bytes = base64.b64decode(im_b64.encode("utf-8"))
            print(f"{img_bytes[:50]=}")

            with open("tmp_image.jpeg", "wb") as file:
                file.write(img_bytes)

        if query and im_b64:
            graph_res = get_bag_by_image_and_text_query(text_query=query,image_file_path="tmp_image.jpeg")
        if im_b64:
            graph_res = get_bag_by_image(image_file_path="tmp_image.jpeg")

        documents = (
            db.collection("Bags")
            .where(filter=FieldFilter("id", "in", graph_res["results"]))
            .get()
        )
        documents = [d.to_dict() for d in documents]

    if request.method == "GET":
        query = request.args.get("query")

        if query:
            print("filtering bags...")
            graph_res = get_bag_by_text_query(text_query=query)
            documents = (
                db.collection("Bags")
                .where(filter=FieldFilter("id", "in", graph_res["results"]))
                .get()
            )
            documents = [d.to_dict() for d in documents]

        else:
            print("fetching all bags...")

            documents = get_all_documents_from_firestore()

    filtered_bags = documents

    return jsonify(filtered_bags)


def get_all_documents_from_firestore() -> List[Dict[str, str]]:

    data = db.collection("Bags").stream()
    documents = [d.to_dict() for d in data]

    return documents


if __name__ == "__main__":
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    app.run(host="0.0.0.0", debug=False, port=8080)
