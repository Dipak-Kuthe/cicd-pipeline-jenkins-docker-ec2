"""Minimal Flask application used to demonstrate the CI/CD pipeline."""
import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return (
        "<h1>CI/CD Demo App</h1>"
        f"<p>Deployed via Jenkins + Docker on host: <b>{socket.gethostname()}</b></p>"
        f"<p>Build: {os.environ.get('BUILD_NUMBER', 'local')}</p>"
    )


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
