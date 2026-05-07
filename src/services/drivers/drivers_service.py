from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient


driversMysql = Blueprint("driversMysql", __name__)

# GET all drivers
@driversMysql.route("/mysql/drivers", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, driverRef, number, code, forename, surname,
            DATE_FORMAT(dob, '%Y-%m-%d') as dob,
            nationality, TRIM(url) as url
            FROM driver
        """)
        drivers = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(drivers)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET driver by id
@driversMysql.route("/mysql/drivers/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, driverRef, number, code, forename, surname,
            DATE_FORMAT(dob, '%Y-%m-%d') as dob,
            nationality, TRIM(url) as url
            FROM driver WHERE id = %s
        """, (id,))
        driver = cursor.fetchone()
        cursor.close()
        db.close()
        if driver:
            return jsonify(driver)
        return jsonify({"error": "Driver not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE driver
@driversMysql.route("/mysql/drivers", methods=["POST"])
def create_driver():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO driver (driverRef, number, code, forename, surname, dob, nationality, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (data["driverRef"], data["number"], data["code"], data["forename"], data["surname"], data["dob"], data["nationality"], data["url"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Driver created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE driver
@driversMysql.route("/mysql/drivers/<int:id>", methods=["PUT"])
def update_driver(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE driver SET driverRef=%s, number=%s, code=%s,
            forename=%s, surname=%s, dob=%s, nationality=%s, url=%s
            WHERE id=%s
        """, (data["driverRef"], data["number"], data["code"], data["forename"], data["surname"], data["dob"], data["nationality"], data["url"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Driver updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE driver
@driversMysql.route("/mysql/drivers/<int:id>", methods=["DELETE"])
def delete_driver(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM driver WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Driver deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})
    


mongo_drivers = MongoClient("mongodb://mongo_drivers:27017")["drivers_db"]

@driversMysql.route("/migrate/drivers", methods=["POST"])
def migrate_drivers():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, driverRef, number, code, forename, surname,
            DATE_FORMAT(dob, '%Y-%m-%d') as dob,
            nationality, TRIM(url) as url
            FROM driver
        """)
        drivers = cursor.fetchall()
        cursor.close()
        db.close()

        mongo_drivers["drivers"].delete_many({})
        result = mongo_drivers["drivers"].insert_many(drivers)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(result.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})