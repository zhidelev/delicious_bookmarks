from flask import Flask, request

app = Flask(__name__)

@app.route("/get_all")
def get_all():
    return "all links"

@app.route("/create", methods=['POST'])
def create():
    print(request)
    return "", 201