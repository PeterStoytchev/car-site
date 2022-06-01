import os
import mysql.connector
from flask import Flask, jsonify, request

import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

# TODO: Fix the direct uses of a user provided variable, in SQL statements


# The zero here, is just a placeholder value, until someone calls a route and touches a route,
# and creates a connection to the db
db = 0

def getcursor():
    global db
    
    try:
        c = db.cursor()
        return c
    except Exception as e:
        db = mysql.connector.connect(
            host= os.environ["dbHost"],
            user= os.environ["dbUser"],
            password= os.environ["dbPasswd"],
            database= os.environ["dbName"],
            connect_timeout=28800
        )

        c = db.cursor()
        return c


def sqlfetch(query, cursor=-1):
    if cursor == -1:
        cursor = getcursor()

    cursor.execute(query)
    return cursor.fetchall()

@app.route("/brands", methods=["GET"])
def getbrands():
    data = sqlfetch(f"""SELECT * FROM brands""")
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
    
    cursor = getcursor()
    for x in models:
        data = sqlfetch(f"""SELECT adid,model,year,km FROM cars WHERE model = {x[0]}""", cursor)
        for y in data:
            img = sqlfetch(f"""SELECT imgsrc FROM imglist WHERE adid = {y[0]} ORDER BY imgid ASC""", cursor)[0][0]
            cars.append(
                {
                    "id": y[0],
                    "model": y[1],
                    "year": y[2],
                    "km": y[3],
                    "img": img
                })


    return jsonify(cars)


@app.route("/brandfromad/<id>")
def getcarfrombrand(id):
    
    cursor = getcursor()

    modelid = sqlfetch(f"""SELECT model FROM cars WHERE adid = {id}""", cursor)[0][0]
    brandid = sqlfetch(f"""SELECT brand FROM models WHERE modelid = {modelid}""", cursor)[0][0]

    return jsonify({"brandid": brandid})

@app.route("/car/<id>", methods=["GET"])
def getcar(id):
    
    cursor = getcursor()
    
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
    cursor = getcursor()

    req = request.json

    insert_sql = """INSERT INTO `cars`(`model`, `year`, `km`, `cardescr`) VALUES (%s,%s,%s,%s)"""
    vals = (req["model"], req["year"], req["km"], req["cardescr"])

    try:
        cursor.execute(insert_sql, vals)
        db.commit()
    except Exception as e:
        app.logger.info(f"Exception when trying to add a new car to the site:\n{e}")
        return "500"

    index = sqlfetch(f"SELECT adid FROM cars ORDER BY adid DESC LIMIT 1", cursor)[0][0]

    insert_sql_img = """INSERT INTO imglist(adid,imgsrc) VALUES (%s,%s)"""
    for x in req["imgsrc"]:
        vals_img = (index, x)
        cursor.execute(insert_sql_img, vals_img)

    db.commit()

    return jsonify({"adid": index})

@app.route("/edit/<id>", methods=["POST"])
def editcar(id):
    cursor = getcursor()
    req = request.json

    update_sql = """UPDATE cars SET model=%s, year=%s, km=%s, cardescr=%s WHERE adid=%s"""
    vals = (req["model"], req["year"], req["km"], req["cardescr"], id)

    try:
        cursor.execute(update_sql, vals)
        db.commit()
    except Exception as e:
        app.logger.info(f"Exception when trying to add a new car to the site:\n{e}")
        return "Exception when trying to add a new car to the site!", 500

    db.commit()
    return "", 200

@app.route("/img", methods=["POST"])
def uploadimg():
    req = request.json
    
    cursor = getcursor()

    insert_sql = """INSERT INTO imglist(adid,imgsrc) VALUES (%s,%s)"""
    vals = (req["adid"], req["imgsrc"])

    try:
        cursor.execute(insert_sql, vals)
        db.commit()
    except Exception as e:
        app.logger.info(f"Exception when trying to add a new img to the site:\n{e}")
        return "500"

    return "200"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)