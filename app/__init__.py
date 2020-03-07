from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object("app.config.DevelopmentConfig")


@app.route("/ping", methods=["GET"])
def ping_ping():
    return jsonify({"message": "pong", "status": "success"})
