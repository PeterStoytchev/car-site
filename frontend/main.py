import os
import requests
import json
from flask import Flask, request, render_template, send_file, send_from_directory

app = Flask(__name__)

#ENDP = "127.0.0.1:8080"

ENDP = os.environ["ENDPOINT"]
API_ENDPOINT = f"http://{ENDP}"

@app.route("/static/<path:path>", methods=["GET"])
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/", methods=["GET"])
def root():
    content = json.loads(requests.get(f'{API_ENDPOINT}/brands').content)
    names = content["names"]
    ids = content["ids"]

    if "brand" in request.args:
        brand = request.args["brand"]
        year = request.args["year"] if "year" in request.args else None
        km = request.args["km"] if "km" in request.args else None

        carlist = json.loads(requests.get(f"{API_ENDPOINT}/carlist/{brand}").content)
        found=[]
        for car in carlist:
            add=False
            if not year == None:
                if car["year"] <= int(year):
                    add=True
        
            if not km == None:
                if car["km"] <= int(km):
                    add=True
                else:
                    add=False
            if add:
                found.append(car)


    return render_template("index.html", brands=names, ids=ids, cars=found)

def findNameFromId(id, ids, names):
    for x in range(len(ids)):
        if int(id) == int(ids[x]):
            return names[x]

def getBrandName(id):
    brandContent = json.loads(requests.get(f"{API_ENDPOINT}/brands").content)
    brandIds = brandContent["ids"]
    brandNames = brandContent["names"]
    return findNameFromId(id, brandIds, brandNames)


@app.route("/brand/<id>", methods=["GET"])
def brand(id):
    model_data = json.loads(requests.get(f"{API_ENDPOINT}/models/{id}").content)

    model_ids = model_data["ids"]
    model_names = model_data["names"]

    content = json.loads(requests.get(f"{API_ENDPOINT}/carlist/{id}").content)

    brandName = getBrandName(id)

    for x in content:
        x["model"] = findNameFromId(x["model"], model_ids, model_names)

    return render_template("brand.html", cars=content, brand=brandName)

@app.route("/car/<id>", methods=["GET"])
def car(id):
    brandid = json.loads(requests.get(f"{API_ENDPOINT}/brandfromad/{id}").content)["brandid"]
    brandName = getBrandName(brandid)

    car = json.loads(requests.get(f"{API_ENDPOINT}/car/{id}").content)

    return render_template("car.html", car=car, brand=brandName)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")