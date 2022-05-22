import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

db = mysql.connector.connect(
    host = "192.168.1.10",
    user = "yoship",
    password = "ffx1v1sagoodgame",
    database = "carsite"
)

def sqlfetch(query, cursor=-1):
    if cursor == -1:
        cursor = db.cursor()

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/brands", methods=["GET"])
def getbrands():
    data = sqlfetch(f"""SELECT * FROM brands""")
    return jsonify(data)


@app.route("/models/<brand_id>", methods=["GET"])
def getmodelsfrombrand(brand_id):
    data = sqlfetch(f"""SELECT modelid,modelname FROM models WHERE brand = {brand_id}""")
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

@app.route("/carlist/<brand_id>", methods=["GET"])
def getcarlist(brand_id):
    models = sqlfetch(f"""SELECT modelid FROM models WHERE brand = {brand_id}""")

    cars = []

    #TODO: Batch execution of querries!
    cursor = db.cursor()
    for x in models:
        data = sqlfetch(f"""SELECT adid,model,year,km FROM cars WHERE model = {x[0]}""", cursor)
        for y in data:
            cars.append(y)


    return jsonify(cars)


@app.route("/car/<id>", methods=["GET"])
def getcar(id):
    cursor = db.cursor()
    
    data = sqlfetch(f"""SELECT * FROM `cars` WHERE `adid` = {id}""", cursor)[0]

    modeldata = sqlfetch(f"SELECT brand,modelname FROM models WHERE modelid = {data[1]}", cursor)[0]
    model = modeldata[1]

    brand = sqlfetch(f"SELECT name FROM brands WHERE carid = {modeldata[0]}", cursor)[0][0]

    imgs = [] 
    for x in sqlfetch(f"SELECT imgsrc FROM imglist WHERE adid = {data[0]}", cursor):
        imgs.append(x[0])

    return jsonify(
    {
        "brand": brand,
        "model": model,
        "year": data[2],
        "km": data[3],
        "cardescr": data[4],
        "imgs": imgs
    })

@app.route("/car", methods=["POST"])
def insertcar():
    cursor = db.cursor()
    req = request.json

    insert_sql = """INSERT INTO `cars`(`model`, `year`, `km`, `cardescr`) VALUES (%s,%s,%s,%s)"""
    vals = (req["model"], req["year"], req["km"], req["cardescr"])

    try:
        cursor.execute(insert_sql, vals)
        db.commit()
    except Exception as e:
        print(f"Exception when trying to add a new car to the site:\n{e}")
        return "500"

    index = sqlfetch(f"SELECT adid FROM cars ORDER BY adid DESC LIMIT 1", cursor)[0][0]

    insert_sql_img = """INSERT INTO imglist(adid,imgsrc) VALUES (%s,%s)"""
    for x in req["imgsrc"]:
        vals_img = (index, x)
        cursor.execute(insert_sql_img, vals_img)

    db.commit()

    return jsonify({"adid": index})

@app.route("/img", methods=["POST"])
def uploadimg():
    req = request.json
    cursor = db.cursor()

    insert_sql = """INSERT INTO imglist(adid,imgsrc) VALUES (%s,%s)"""
    vals = (req["adid"], req["imgsrc"])

    try:
        cursor.execute(insert_sql, vals)
        db.commit()
    except Exception as e:
        print(f"Exception when trying to add a new img to the site:\n{e}")
        return "500"

    return "200"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")