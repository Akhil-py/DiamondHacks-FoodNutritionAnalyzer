from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# @app.route('/search', methods = ['GET'])
# def search_products():
#     search_term = request.agrs.get('query', '')
#     if not search_term:
#         return jsonify({"error":"No search term provided"}), 400
#     product_data = search(search_term)
#     return jsonify(product_data)

@app.route("/")
def home():
    return render_template("another1.html")


@app.route("/about")
def about():
    return render_template("about.html")

# if __name__ == '__main__':
#     app.run(debug = True)
