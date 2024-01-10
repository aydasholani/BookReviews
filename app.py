from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def Homepage():
    return jsonify({"status": 200, "message": "Success"})
