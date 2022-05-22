import requests
import json
from flask import Flask, render_template, send_file, send_from_directory

app = Flask(__name__)

@app.route("/static/<path:path>", methods=["GET"])
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/", methods=["GET"])
def root():
    content = json.loads(requests.get('http://127.0.0.1:5001/brands').content)
    names = content["names"]
    ids = content["ids"]

    return render_template("index.html", brands=names, ids=ids)

def findNameFromId(id, ids, names):
    for x in range(len(ids)):
        if int(id) == int(ids[x]):
            return names[x]

def getBrandName(id):
    brandContent = json.loads(requests.get(f"http://127.0.0.1:5001/brands").content)
    brandIds = brandContent["ids"]
    brandNames = brandContent["names"]
    return findNameFromId(id, brandIds, brandNames)


@app.route("/brand/<id>", methods=["GET"])
def brand(id):
    model_data = json.loads(requests.get(f"http://127.0.0.1:5001/models/{id}").content)
    
    model_ids = model_data["ids"]
    model_names = model_data["names"]
    content = json.loads(requests.get(f"http://127.0.0.1:5001/carlist/{id}").content)
    
    brandName = getBrandName(id)

    for x in content:
        x["model"] = findNameFromId(x["model"], model_ids, model_names)

    return render_template("brand.html", cars=content, brand=brandName)

@app.route("/car/<id>", methods=["GET"])
def car(id):
    brandid = json.loads(requests.get(f"http://127.0.0.1:5001//brandfromad/{id}").content)["brandid"]
    brandName = getBrandName(brandid)

    car = json.loads(requests.get(f"http://127.0.0.1:5001/car/{id}").content)

    return render_template("car.html", car=car, brand=brandName)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")