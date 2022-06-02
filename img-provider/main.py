import os
import requests
import json
from flask import Flask, render_template, send_file, send_from_directory

app = Flask(__name__)

"""
@app.route("/static/<path:path>", methods=["GET"])
def serve_static(path):
    return send_from_directory("static", path)
"""

@app.route("/", methods=["POST"])
def root():
    return "", 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")