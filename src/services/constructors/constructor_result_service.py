from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

constructorResultMysql = Blueprint("constructorResultMysql", __name__)
mongo_constructors = MongoClient("mongodb://mongo_constructors:27017")["constructors_db"]

# GET all constructorResults
@constructorResultMysql.route("/mysql/constructorResults", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructorResult")
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET constructorResult by id
@constructorResultMysql.route("/mysql/constructorResults/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructorResult WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return jsonify(result)
        return jsonify({"error": "Constructor result not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE constructorResult
@constructorResultMysql.route("/mysql/constructorResults", methods=["POST"])
def create_result():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO constructorResult (race_id, constructor_id, points)
            VALUES (%s, %s, %s)
        """, (data["race_id"], data["constructor_id"], data["points"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Constructor result created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE constructorResult
@constructorResultMysql.route("/mysql/constructorResults/<int:id>", methods=["PUT"])
def update_result(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE constructorResult SET race_id=%s, constructor_id=%s, points=%s
            WHERE id=%s
        """, (data["race_id"], data["constructor_id"], data["points"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Constructor result updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE constructorResult
@constructorResultMysql.route("/mysql/constructorResults/<int:id>", methods=["DELETE"])
def delete_result(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM constructorResult WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Constructor result deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})


# MIGRATE constructorResults to MongoDB
@constructorResultMysql.route("/migrate/constructorResults", methods=["POST"])
def migrate_constructor_results():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT cr.id, cr.points,
            r.id as race_id, r.year, r.round, r.name as race_name,
            r.date as race_date,
            c.id as constructor_id, c.constructorName, c.constructorRef,
            c.constructorNationality, TRIM(c.constructorUrl) as constructorUrl
            FROM constructorResult cr
            JOIN race r ON cr.race_id = r.id
            JOIN constructor c ON cr.constructor_id = c.id
        """)
        results = cursor.fetchall()
        cursor.close()
        db.close()

        for result in results:
            result["points"] = float(result["points"]) if result["points"] else None
            result["race"] = {
                "id": result.pop("race_id"),
                "year": result.pop("year"),
                "round": result.pop("round"),
                "name": result.pop("race_name"),
                "date": str(result.pop("race_date"))
            }
            result["constructor"] = {
                "id": result.pop("constructor_id"),
                "name": result.pop("constructorName"),
                "ref": result.pop("constructorRef"),
                "nationality": result.pop("constructorNationality"),
                "url": result.pop("constructorUrl")
            }

        mongo_constructors["constructorResults"].delete_many({})
        inserted = mongo_constructors["constructorResults"].insert_many(results)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(inserted.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
