from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

qualifyingMysql = Blueprint("qualifyingMysql", __name__)
mongo_results = MongoClient("mongodb://mongo_results:27017")["results_db"]

# GET all qualifying
@qualifyingMysql.route("/mysql/qualifying", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM qualifying")
        qualifying = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(qualifying)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET qualifying by id
@qualifyingMysql.route("/mysql/qualifying/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM qualifying WHERE id = %s", (id,))
        qualifying = cursor.fetchone()
        cursor.close()
        db.close()
        if qualifying:
            return jsonify(qualifying)
        return jsonify({"error": "Qualifying not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE qualifying
@qualifyingMysql.route("/mysql/qualifying", methods=["POST"])
def create_qualifying():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO qualifying (race_id, driver_id, constructor_id, number, positionQualifyer, q1, q2, q3)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (data["race_id"], data["driver_id"], data["constructor_id"], data["number"],
              data["positionQualifyer"], data["q1"], data["q2"], data["q3"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Qualifying created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE qualifying
@qualifyingMysql.route("/mysql/qualifying/<int:id>", methods=["PUT"])
def update_qualifying(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE qualifying SET race_id=%s, driver_id=%s, constructor_id=%s,
            number=%s, positionQualifyer=%s, q1=%s, q2=%s, q3=%s
            WHERE id=%s
        """, (data["race_id"], data["driver_id"], data["constructor_id"], data["number"],
              data["positionQualifyer"], data["q1"], data["q2"], data["q3"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Qualifying updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE qualifying
@qualifyingMysql.route("/mysql/qualifying/<int:id>", methods=["DELETE"])
def delete_qualifying(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM qualifying WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Qualifying deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})


# MIGRATE qualifying to MongoDB
@qualifyingMysql.route("/migrate/qualifying", methods=["POST"])
def migrate_qualifying():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT q.id, q.number, q.positionQualifyer, q.q1, q.q2, q.q3,
            r.id as race_id, r.year, r.round, r.name as race_name,
            r.date as race_date,
            d.id as driver_id, d.driverRef, d.forename, d.surname,
            d.dob as driver_dob, d.nationality as driver_nationality,
            c.id as constructor_id, c.constructorName, c.constructorRef,
            c.constructorNationality
            FROM qualifying q
            JOIN race r ON q.race_id = r.id
            JOIN driver d ON q.driver_id = d.id
            JOIN constructor c ON q.constructor_id = c.id
        """)
        qualifying = cursor.fetchall()
        cursor.close()
        db.close()

        for row in qualifying:
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

        mongo_results["qualifying"].delete_many({})
        inserted = mongo_results["qualifying"].insert_many(qualifying)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(inserted.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
