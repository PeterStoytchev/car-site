import os
import requests
import json
from flask import Flask, request, render_template, send_file, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

#ENDP = "127.0.0.1:8080"

ENDP = os.environ["ENDPOINT"]
API_ENDPOINT = f"http://{ENDP}"

@app.route("/static/<path:path>", methods=["GET"])
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/", methods=["GET", "DELETE"])
def root():
    if request.method == "DELETE":
        carId=request.args.get("carId")
        requests.delete(f"{API_ENDPOINT}/deletecar/" + carId)
        return redirect(url_for("root"))

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
            if not km == None and add == True:
                if car["km"] <= int(km):
                    add=True
                else:
                    add=False

            if add:
                found.append(car)
        return render_template("index.html", brands = names, ids= ids, cars=found)

    return render_template("index.html", brands=names, ids=ids)

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

@app.route("/new", methods=["GET", "POST"])
def adadd():
    if request.method == "GET":
        content = json.loads(requests.get(f'{API_ENDPOINT}/brands').content)
        names = content["names"]
        ids = content["ids"]
        if "brandId" in request.args:
            brandId= request.args["brandId"]
        else:
            brandId= ids[0]
        
        print("brandId", brandId)
        models=json.loads(requests.get(f"{API_ENDPOINT}/models/{brandId}").content)
        modelNames= models["names"]
        modelIds= models["ids"]

        return render_template("addad.html", 
            brands=names, 
            ids=ids, 
            modelNames=modelNames, 
            modelIds=modelIds, 
            brandId=int(brandId))
    elif request.method == "POST":
        requiredArgs=["brand", "model", "year", "km", "desc", "email"]
        for arg in requiredArgs:
            if request.form.get(arg) == None:
                return redirect(url_for("adadd", message="Please fill out the " + arg + "field"))

        brand = request.form.get("brand")
        model = request.form.get("model")
        year = request.form.get("year")
        km = request.form.get("km")
        desc = request.form.get("desc")
        email = request.form.get("email")

        if 'img' not in request.files:
            print("UNHANDLED ERROR")
        file = request.files['img']
        if file.filename == '':
            print("UNHANDLED ERROR")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save("static/uploads/" + filename)

        files=[]
        files.append(filename)
        data = {
            "model": int(model),
            "year": int(year),
            "km": int(km),
            "cardescr": desc,
            "email": email,
            "imgsrc": files
        }
        resp = requests.post(f"{API_ENDPOINT}/car", data=data)

        if "adid" not in str(resp.content):
            print("ERROR")
        
        return redirect(url_for("root") + "?posted=true")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")