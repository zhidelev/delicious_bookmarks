from flask import Flask, request

app = Flask(__name__)


@app.route("/get_all")
def get_all():
    return "all links"


@app.route("/create", methods=["POST"])
def create():
    print(request)
    return "", 201


@app.route("/get_one/{link_id}")
def get_one():
    return "one link"


@app.route("/delete/{link_id}")
def delete():
    return "link is deleted"


@app.route("/archive/{link_id}")
def archive():
    return "link in archive"
