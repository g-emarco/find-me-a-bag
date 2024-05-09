from typing import List, Dict

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, render_template, request

from agent.main import compiled_graph

load_dotenv()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_bag_by_text_query(text_query: str):
    return compiled_graph.invoke({"query": text_query})


@app.route("/bags")
def get_bags():
    query = request.args.get("query")

    if query:
        print("filtering bags...")
        documents = get_bag_by_text_query(text_query=query)
    else:
        print("fetching all bags...")

        documents = get_all_documents_from_firestore()

    filtered_bags = documents

    return jsonify(filtered_bags)


def get_all_documents_from_firestore() -> List[Dict[str, str]]:

    data = db.collection("bags").stream()
    documents = [d.to_dict() for d in data]

    return documents


if __name__ == "__main__":
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    app.run(host="0.0.0.0", debug=False, port=8080)
