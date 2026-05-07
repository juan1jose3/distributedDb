from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

constructorStandingMysql = Blueprint("constructorStandingMysql", __name__)
mongo_constructors = MongoClient("mongodb://mongo_constructors:27017")["constructors_db"]

# GET all constructorStandings
@constructorStandingMysql.route("/mysql/constructorStandings", methods=["GET"])
def get_all():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructorStanding")
        standings = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(standings)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET constructorStanding by id
@constructorStandingMysql.route("/mysql/constructorStandings/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM constructorStanding WHERE id = %s", (id,))
        standing = cursor.fetchone()
        cursor.close()
        db.close()
        if standing:
            return jsonify(standing)
        return jsonify({"error": "Standing not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# CREATE constructorStanding
@constructorStandingMysql.route("/mysql/constructorStandings", methods=["POST"])
def create_standing():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO constructorStanding (race_id, constructor_id, points, positionConstructor, wins)
            VALUES (%s, %s, %s, %s, %s)
        """, (data["race_id"], data["constructor_id"], data["points"], data["positionConstructor"], data["wins"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Standing created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})

# UPDATE constructorStanding
@constructorStandingMysql.route("/mysql/constructorStandings/<int:id>", methods=["PUT"])
def update_standing(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE constructorStanding SET race_id=%s, constructor_id=%s,
            points=%s, positionConstructor=%s, wins=%s
            WHERE id=%s
        """, (data["race_id"], data["constructor_id"], data["points"], data["positionConstructor"], data["wins"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Standing updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

# DELETE constructorStanding
@constructorStandingMysql.route("/mysql/constructorStandings/<int:id>", methods=["DELETE"])
def delete_standing(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM constructorStanding WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Standing deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})