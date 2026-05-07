from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

driverStandingMysql = Blueprint("driverStandingMysql", __name__)

# GET all driverStandings
@driverStandingMysql.route("/mysql/driverStandings", methods=["GET"])
def get_all_standings():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM driverStandings")
        standings = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(standings)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET driverStanding by id
@driverStandingMysql.route("/mysql/driverStandings/<int:id>", methods=["GET"])
def get_standing_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM driverStandings WHERE id = %s", (id,))
        standing = cursor.fetchone()
        cursor.close()
        db.close()
        if standing:
            return jsonify(standing)
        return jsonify({"error": "Standing not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE driverStanding
@driverStandingMysql.route("/mysql/driverStandings", methods=["POST"])
def create_standing():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO driverStandings (race_id, driver_id, points, position, positionText, wins)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data["race_id"], data["driver_id"], data["points"], data["position"], data["positionText"], data["wins"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Standing created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE driverStanding
@driverStandingMysql.route("/mysql/driverStandings/<int:id>", methods=["PUT"])
def update_standing(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE driverStandings SET race_id=%s, driver_id=%s, points=%s,
            position=%s, positionText=%s, wins=%s
            WHERE id=%s
        """, (data["race_id"], data["driver_id"], data["points"], data["position"], data["positionText"], data["wins"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Standing updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE driverStanding
@driverStandingMysql.route("/mysql/driverStandings/<int:id>", methods=["DELETE"])
def delete_standing(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM driverStandings WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Standing deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

mongo_drivers = MongoClient("mongodb://mongo_drivers:27017")["drivers_db"]

@driverStandingMysql.route("/migrate/driverStandings", methods=["POST"])
def migrate_driver_standings():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM driverStandings")
        standings = cursor.fetchall()
        cursor.close()
        db.close()

        # convert Decimal to float
        for standing in standings:
            standing["points"] = float(standing["points"])

        mongo_drivers["driverStandings"].delete_many({})
        result = mongo_drivers["driverStandings"].insert_many(standings)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(result.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})