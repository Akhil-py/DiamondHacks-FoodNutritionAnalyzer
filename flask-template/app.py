from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("another1.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/mainPage")
def mainPage():
    return render_template("home.html")