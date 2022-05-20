import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

db = mysql.connector.connect(
    host = "ls-7c09fd48aca46f6e0c17757e3e538c5e678c5b81.c7bo5hducqb2.eu-central-1.rds.amazonaws.com",
    user = "yoship",
    password = "ffxivisagoodgame",
    database = "dbmaster"
)

@app.route("/car", methods=["POST"])
def insertcar():
    data = request.json
    cursor = db.cursor()

    insert_sql = """INSERT INTO `cars`(`make`, `model`, `year`, `km`, `cardescr`) VALUES (%s,%s,%s,%s,%s)"""
    vals = (data["make"], data["model"], data["year"], data["km"], data["cardescr"])

    try:
        cursor.execute(insert_sql, vals)
        db.commit()
    except Exception as e:
        print(f"Exception when trying to add a new car to the site:\n{e}")
        return "500"

    return "200"

@app.route("/car/<id>", methods=["GET"])
def getcar(id):
    cursor = db.cursor()
    data = cursor.fetchall(f"""SELECT * FROM `cars` WHERE `adid` = {id}""")

    print(type(data))
    print(data)

    return "200"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")