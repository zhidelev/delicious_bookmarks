from flask import Flask

app = Flask(__name__)

@app.route('/get_all')
def get_all():
    return 'all links'