from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

lapTimesMysql = Blueprint("lapTimesMysql", __name__)
mongo_results = MongoClient("mongodb://mongo_results:27017")["results_db"]

# GET all lapTimes
@lapTimesMysql.route("/mysql/lapTimes", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lapTimes")
        lap_times = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(lap_times)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET lapTime by id
@lapTimesMysql.route("/mysql/lapTimes/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lapTimes WHERE id = %s", (id,))
        lap_time = cursor.fetchone()
        cursor.close()
        db.close()
        if lap_time:
            return jsonify(lap_time)
        return jsonify({"error": "Lap time not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE lapTime
@lapTimesMysql.route("/mysql/lapTimes", methods=["POST"])
def create_lap_time():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO lapTimes (race_id, driver_id, lap, lapPosition, lapTime, milliseconds)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data["race_id"], data["driver_id"], data["lap"], data["lapPosition"],
              data["lapTime"], data["milliseconds"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Lap time created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE lapTime
@lapTimesMysql.route("/mysql/lapTimes/<int:id>", methods=["PUT"])
def update_lap_time(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE lapTimes SET race_id=%s, driver_id=%s, lap=%s,
            lapPosition=%s, lapTime=%s, milliseconds=%s
            WHERE id=%s
        """, (data["race_id"], data["driver_id"], data["lap"], data["lapPosition"],
              data["lapTime"], data["milliseconds"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Lap time updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE lapTime
@lapTimesMysql.route("/mysql/lapTimes/<int:id>", methods=["DELETE"])
def delete_lap_time(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM lapTimes WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Lap time deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})


# MIGRATE lapTimes to MongoDB
@lapTimesMysql.route("/migrate/lapTimes", methods=["POST"])
def migrate_lap_times():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT lt.id, lt.lap, lt.lapPosition, lt.lapTime, lt.milliseconds,
            r.id as race_id, r.year, r.round, r.name as race_name,
            r.date as race_date,
            d.id as driver_id, d.driverRef, d.forename, d.surname,
            d.dob as driver_dob, d.nationality as driver_nationality
            FROM lapTimes lt
            JOIN race r ON lt.race_id = r.id
            JOIN driver d ON lt.driver_id = d.id
        """)
        lap_times = cursor.fetchall()
        cursor.close()
        db.close()

        for row in lap_times:
            row["race"] = {
                "id": row.pop("race_id"),
                "year": row.pop("year"),
                "round": row.pop("round"),
                "name": row.pop("race_name"),
                "date": str(row.pop("race_date"))
            }
            row["driver"] = {
                "id": row.pop("driver_id"),
                "ref": row.pop("driverRef"),
                "forename": row.pop("forename"),
                "surname": row.pop("surname"),
                "dob": str(row.pop("driver_dob")) if row.get("driver_dob") else None,
                "nationality": row.pop("driver_nationality")
            }

        mongo_results["lapTimes"].delete_many({})
        inserted = mongo_results["lapTimes"].insert_many(lap_times)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(inserted.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
