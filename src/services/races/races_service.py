from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

selectOne =  Blueprint("selectOne",__name__)

def clean_time(races):
    for race in races:
        race["race_time"] = str(race["race_time"])
        race["date"] = str(race["date"])
    return races

# mysql endpoints

# GET all races
@selectOne.route("/mysql/races", methods=["GET"])
def get_races():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, year, round, circuit_id, name,
            DATE_FORMAT(date, '%Y-%m-%d') as date,
            TIME_FORMAT(race_time, '%H:%i:%s') as race_time,
            TRIM(url) as url
            FROM race
        """)
        races = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(races)
    except Exception as e:
        return jsonify({"error": str(e)})


# GET race by id
@selectOne.route("/mysql/races/<int:id>", methods=["GET"])
def get_race_by_id(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, year, round, circuit_id, name,
            date, race_time, TRIM(url) as url
            FROM race WHERE id = %s
        """, (id,))
        race = cursor.fetchone()
        cursor.close()
        db.close()
        if race:
            races = clean_time(race)
            return jsonify(races)
        return jsonify({"error": "Race not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    

# CREATE
@selectOne.route("/mysql/races", methods=["POST"])
def create_race():
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO race (year, round, circuit_id, name, date, race_time, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data["year"], data["round"], data["circuit_id"], data["name"], data["date"], data["race_time"], data["url"]))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Race created", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)})


# UPDATE
@selectOne.route("/mysql/races/<int:id>", methods=["PUT"])
def update_race(id):
    try:
        data = request.get_json()
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            UPDATE race SET year=%s, round=%s, circuit_id=%s, 
            name=%s, date=%s, race_time=%s, url=%s
            WHERE id=%s
        """, (data["year"], data["round"], data["circuit_id"], data["name"], data["date"], data["race_time"], data["url"], id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Race updated"})
    except Exception as e:
        return jsonify({"error": str(e)})


# DELETE
@selectOne.route("/mysql/races/<int:id>", methods=["DELETE"])
def delete_race(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM race WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Race deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})








# GET races by season
@selectOne.route("/mysql/races/season/<int:year>", methods=["GET"])
def get_races_by_season(year):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, year, round, circuit_id, name,
            date, race_time, TRIM(url) as url
            FROM race WHERE year = %s
            ORDER BY round
        """, (year,))
        races = cursor.fetchall()
        cursor.close()
        db.close()
        
        races = clean_time(races)
        return jsonify(races)
    except Exception as e:
        return jsonify({"error": str(e)})
    

#Migrate to mongodb

mongo_races = MongoClient("mongodb://mongo_races:27017")["races_db"]

@selectOne.route("/migrate/races", methods=["POST"])
def migrate_races():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT r.id, r.year, r.round, r.name,
            r.date, r.race_time, TRIM(r.url) as url,
            c.id as circuit_id, c.circuitName, c.location, 
            c.country, c.lat, c.lng, c.alt, TRIM(c.circuitUrl) as circuitUrl
            FROM race r
            JOIN circuit c ON r.circuit_id = c.id
        """)
        races = cursor.fetchall()
        cursor.close()
        db.close()

      
        for race in races:
            race["date"] = str(race["date"])
            race["race_time"] = str(race["race_time"])
            race["circuit"] = {
                "id": race.pop("circuit_id"),
                "name": race.pop("circuitName"),
                "location": race.pop("location"),
                "country": race.pop("country"),
                "lat": float(race.pop("lat")),      
                "lng": float(race.pop("lng")),      
                "alt": float(race.pop("alt")) if race.get("alt") else None,
                "url": race.pop("circuitUrl")
            }

        # Insert into MongoDB
        mongo_races["races"].delete_many({})
        result = mongo_races["races"].insert_many(races)

        return jsonify({
            "message": "Migration successful",
            "inserted": len(result.inserted_ids)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
