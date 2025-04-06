from flask import Flask, jsonify, request, render_template
from sortingAPI.sorting import search

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("another1.html")

@app.route("/search", methods=["POST"])
def search_products():
    search_term = request.form.get("query", "").strip()
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400

    product_data = search(search_term)

    return render_template("another1.html", results=product_data, query=search_term)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)