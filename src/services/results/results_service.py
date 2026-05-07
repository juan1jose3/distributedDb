from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

resultsMysql = Blueprint("resultsMysql", __name__)
mongo_results = MongoClient("mongodb://mongo_results:27017")["results_db"]

# GET all results
@resultsMysql.route("/mysql/results", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM results")
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET result by id
@resultsMysql.route("/mysql/results/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM results WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return jsonify(result)
        return jsonify({"error": "Result not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE result
@resultsMysql.route("/mysql/results", methods=["POST"])
def create_result():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO results (race_id, driver_id, constructor_id, number, grid,
            position, positionText, positionOrder, points, laps, resultsTime,
            milliseconds, fastestLap, rankResults, fastestLapTime, fastestLapSpeed, status_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data["race_id"], data["driver_id"], data["constructor_id"], data["number"],
              data["grid"], data["position"], data["positionText"], data["positionOrder"],
              data["points"], data["laps"], data["resultsTime"], data["milliseconds"],
              data["fastestLap"], data["rankResults"], data["fastestLapTime"],
              data["fastestLapSpeed"], data["status_id"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Result created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE result
@resultsMysql.route("/mysql/results/<int:id>", methods=["PUT"])
def update_result(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE results SET race_id=%s, driver_id=%s, constructor_id=%s, number=%s,
            grid=%s, position=%s, positionText=%s, positionOrder=%s, points=%s, laps=%s,
            resultsTime=%s, milliseconds=%s, fastestLap=%s, rankResults=%s,
            fastestLapTime=%s, fastestLapSpeed=%s, status_id=%s
            WHERE id=%s
        """, (data["race_id"], data["driver_id"], data["constructor_id"], data["number"],
              data["grid"], data["position"], data["positionText"], data["positionOrder"],
              data["points"], data["laps"], data["resultsTime"], data["milliseconds"],
              data["fastestLap"], data["rankResults"], data["fastestLapTime"],
              data["fastestLapSpeed"], data["status_id"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Result updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE result
@resultsMysql.route("/mysql/results/<int:id>", methods=["DELETE"])
def delete_result(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM results WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Result deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})


# MIGRATE results to MongoDB
@resultsMysql.route("/migrate/results", methods=["POST"])
def migrate_results():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT res.id, res.number, res.grid, res.position, res.positionText,
            res.positionOrder, res.points, res.laps, res.resultsTime,
            res.milliseconds, res.fastestLap, res.rankResults,
            res.fastestLapTime, res.fastestLapSpeed,
            r.id as race_id, r.year, r.round, r.name as race_name,
            r.date as race_date,
            d.id as driver_id, d.driverRef, d.forename, d.surname,
            d.dob as driver_dob, d.nationality as driver_nationality,
            c.id as constructor_id, c.constructorName, c.constructorRef,
            c.constructorNationality,
            s.id as status_id, s.statusName
            FROM results res
            JOIN race r ON res.race_id = r.id
            JOIN driver d ON res.driver_id = d.id
            JOIN constructor c ON res.constructor_id = c.id
            JOIN status s ON res.status_id = s.id
        """)
        results = cursor.fetchall()
        cursor.close()
        db.close()

        for row in results:
            row["points"] = float(row["points"]) if row["points"] else None
            row["fastestLapSpeed"] = float(row["fastestLapSpeed"]) if row["fastestLapSpeed"] else None
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
            row["constructor"] = {
                "id": row.pop("constructor_id"),
                "name": row.pop("constructorName"),
                "ref": row.pop("constructorRef"),
                "nationality": row.pop("constructorNationality")
            }
            row["status"] = {
                "id": row.pop("status_id"),
                "name": row.pop("statusName")
            }

        mongo_results["results"].delete_many({})
        inserted = mongo_results["results"].insert_many(results)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(inserted.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
