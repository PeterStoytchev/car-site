import os, uuid, webp
from flask import Flask, send_from_directory, request
from PIL import Image

app = Flask(__name__)

import logging

logging.basicConfig(level=logging.DEBUG)

@app.route("/<path:path>", methods=["GET"])
def serve_static(path):
    return send_from_directory("imgs", path)

def findCorrectRes(y_wanted, x, y):
    height_percent = (y_wanted / float(y))
    width_size = int((float(x) * float(height_percent)))

    return (int(width_size), int(y_wanted))

@app.route("/<y>", methods=["POST"])
def root(y):
    height = int(y)

    file = request.files['file']
    filename = str(uuid.uuid4().hex)

    tmp_path = os.path.join("imgs", f"{filename}.tmp")
    file.save(tmp_path)

    img = Image.open(tmp_path)
    img = img.resize(findCorrectRes(height, img.width, img.height))
    webp.save_image(img, os.path.join("imgs", f"{filename}.webp"), quality=70)

    os.remove(tmp_path)

    return filename, 200

if __name__ == "__main__":
    dirname = "imgs"
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    app.run(debug=False, host="0.0.0.0")