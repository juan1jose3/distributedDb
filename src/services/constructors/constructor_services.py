from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

constructorsMysql = Blueprint("constructorsMysql", __name__)
mongo_constructors = MongoClient("mongodb://mongo_constructors:27017")["constructors_db"]

# GET all constructors
@constructorsMysql.route("/mysql/constructors", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructor")
        constructors = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(constructors)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET constructor by id
@constructorsMysql.route("/mysql/constructors/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructor WHERE id = %s", (id,))
        constructor = cursor.fetchone()
        cursor.close()
        db.close()
        if constructor:
            return jsonify(constructor)
        return jsonify({"error": "Constructor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE constructor
@constructorsMysql.route("/mysql/constructors", methods=["POST"])
def create_constructor():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO constructor (constructorName, constructorRef, constructorNationality, constructorUrl)
            VALUES (%s, %s, %s, %s)
        """, (data["constructorName"], data["constructorRef"], data["constructorNationality"], data["constructorUrl"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Constructor created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE constructor
@constructorsMysql.route("/mysql/constructors/<int:id>", methods=["PUT"])
def update_constructor(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE constructor SET constructorName=%s, constructorRef=%s,
            constructorNationality=%s, constructorUrl=%s
            WHERE id=%s
        """, (data["constructorName"], data["constructorRef"], data["constructorNationality"], data["constructorUrl"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Constructor updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE constructor
@constructorsMysql.route("/mysql/constructors/<int:id>", methods=["DELETE"])
def delete_constructor(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM constructor WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Constructor deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})
    




# MIGRATE constructors to MongoDB
@constructorsMysql.route("/migrate/constructors", methods=["POST"])
def migrate_constructors():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructor")
        constructors = cursor.fetchall()
        cursor.close()
        db.close()

        mongo_constructors["constructors"].delete_many({})
        result = mongo_constructors["constructors"].insert_many(constructors)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(result.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})