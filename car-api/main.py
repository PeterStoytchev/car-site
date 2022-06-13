import os, logging, requests
from DatabaseAssistant import DatabaseAssistant
from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

IMG_ENDPOINT = os.environ["IMG_ENDPOINT"]

db = DatabaseAssistant()

@app.route("/brands", methods=["GET"])
def getbrands():
    data = db.ReadQuery("SELECT * FROM brands")
    ids = []
    names = []

    for x in data:
        ids.append(x[0])
        names.append(x[1])

    return jsonify(
    {
        "ids": ids,
        "names": names
    })

@app.route("/models/<brand_id>", methods=["GET"])
def getmodelsfrombrand(brand_id):
    if not brand_id.isdigit():
        return "Invalid adid provided!", 400 
    else:
        brand_id = int(brand_id)

    data = db.ReadQuery("SELECT modelid,modelname FROM models WHERE brand = %s", [brand_id])
    ids = []
    names = []

    for x in data:
        ids.append(x[0])
        names.append(x[1])

    return jsonify(
        {
            "ids": ids,
            "names": names
        }
    )

# TODO: THIS ONE IS REALLY SLOW
@app.route("/carlist/<brand_id>", methods=["GET"])
def getcarlist(brand_id):
    if not brand_id.isdigit():
        return "Invalid adid provided!", 400 
    else:
        brand_id = int(brand_id)

    models = db.ReadQuery("SELECT modelid FROM models WHERE brand = %s", [brand_id])

    cars = []
    for x in models:
        data = db.ReadQuery("SELECT adid,model,year,km,bhp,email,price FROM cars WHERE model = %s", [x[0]])
        for y in data:
            try:
                img = db.ReadQuery("SELECT imgsrc FROM imglist WHERE adid = %s ORDER BY imgid ASC", [y[0]])[0][0]
                img = str(requests.get(f"http://{IMG_ENDPOINT}/{img}").content).split("'")[1]
            except Exception as e:
                img = ""
            cars.append(
                {
                    "id": y[0],
                    "model": y[1],
                    "year": y[2],
                    "km": y[3],
                    "img": img,
                    "bhp": y[4],
                    "email": y[5],
                    "price": y[6]
                })


    return jsonify(cars)


@app.route("/brandfromad/<id>")
def getcarfrombrand(id):
    if not id.isdigit():
        return "Invalid adid provided!", 400 
    else:
        id = int(id)

    modelid = db.ReadQuery("SELECT model FROM cars WHERE adid = %s", [id])[0][0]
    brandid = db.ReadQuery("SELECT brand FROM models WHERE modelid = %s", [modelid])[0][0]

    return jsonify({"brandid": brandid})

@app.route("/car/<id>", methods=["GET"])
def getcar(id):
    if not id.isdigit():
        return "Invalid adid provided!", 400 
    else:
        id = int(id)
    
    data = db.ReadQuery("SELECT * FROM cars WHERE adid = %s", [id])[0]

    modeldata = db.ReadQuery("SELECT brand,modelname FROM models WHERE modelid = %s", [data[1]])[0]
    model = modeldata[1]

    brand = db.ReadQuery("SELECT name FROM brands WHERE carid = %s", [modeldata[0]])[0][0]

    imgs = [] 
    for x in db.ReadQuery("SELECT imgsrc FROM imglist WHERE adid = %s", [data[0]]):
        actual_link = str(requests.get(f"http://{IMG_ENDPOINT}/{x[0]}").content).split("'")[1]
        imgs.append(actual_link)

    return jsonify(
    {
        "brand": brand,
        "model": model,
        "year": data[2],
        "km": data[3],
        "bhp": data[4],
        "price": data[5],
        "cardescr": data[6],
        "email": data[7],
        "imgs": imgs
    })

@app.route("/car", methods=["POST"])
def insertcar():
    req = request.json

    insert_sql = "INSERT INTO cars(model, year, km, bhp, email, price, cardescr) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    vals = (req["model"], req["year"], req["km"], req["bhp"], req["email"], req["price"], req["cardescr"])

    try:
        db.WriteQuery(insert_sql, vals)
    except Exception as e:
        app.logger.info(f"Exception when trying to add a new car to the site:\n{e}")
        return "500"

    index = db.ReadQueryMaster("SELECT adid FROM cars ORDER BY adid DESC LIMIT 1")[0][0]

    insert_sql_img = "INSERT INTO imglist(adid,imgsrc) VALUES (%s,%s)"
    for x in req["imgsrc"]:
        vals_img = (index, x)
        db.WriteQuery(insert_sql_img, vals_img)

    return jsonify({"adid": index})

@app.route("/edit/<id>", methods=["POST"])
def editcar(id):
    if not id.isdigit():
        return "Invalid adid provided!", 400
    else:
        id = int(id)

    req = request.json

    update_sql = "UPDATE cars SET model=%s, year=%s, km=%s, cardescr=%s, price=%s, email=%s, bhp=%s WHERE adid=%s"
    vals = (req["model"], req["year"], req["km"], req["cardescr"], req["price"], req["email"], req["bhp"], id)

    try:
        db.WriteQuery(update_sql, vals)
    except Exception as e:
        app.logger.info(f"Exception when trying to add a new car to the site:\n{e}")
        return "Exception when trying to add a new car to the site!", 500

    return "", 200

@app.route("/deluser", methods=["DELETE"])
def deluser():
    req = request.json
    
    for x in db.ReadQuery("SELECT adid FROM cars WHERE email = %s", [req["email"]]):
        for y in db.ReadQuery("SELECT imgsrc FROM imglist WHERE adid = %s", [x[0]]):
            requests.delete(f"http://{IMG_ENDPOINT}/{y[0]}")
           
        db.WriteQuery("DELETE FROM imglist WHERE adid = %s", [x[0]])
    
    db.WriteQuery("DELETE FROM cars WHERE email = %s", [req["email"]])

    return "", 200