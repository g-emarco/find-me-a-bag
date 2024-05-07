from dotenv import load_dotenv
import json
from flask import Flask, render_template, request, jsonify

from agent.main import compiled_graph

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bags")
def get_bags():
    query = request.args.get("query")

    if query:
        print("filtering bags...")

        bag_data = compiled_graph.invoke({"query": query})
    else:
        print("fetching all bags...")
        with open("bags.json", "r") as f:
            bag_data = json.load(f)

    filtered_bags = bag_data

    return jsonify(filtered_bags)


if __name__ == "__main__":
    app.run(debug=True)
