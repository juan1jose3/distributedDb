from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient


racesMongo = Blueprint("racesMongo",__name__)


mongo_races = MongoClient("mongodb://mongo_races:27017")["races_db"]

@racesMongo.route("/mongo/races/<int:id>", methods=["GET"])
def get_race_by_id(id):
    try:
        race = mongo_races["races"].find_one({"id": id}, {"_id": 0})
        if race:
            return jsonify(race)
        return jsonify({"error": "Race not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    
@racesMongo.route("/mongo/races",methods=["GET"])
def get_all_races():
    try:
        races = list(mongo_races["races"].find({}, {"_id": 0}))
        return jsonify(races)
    except Exception as e:
        return jsonify({"error": str(e)})
    

@racesMongo.route("/mongo/races/count", methods=["GET"])
def count_races():
    try:
        count = mongo_races["races"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
    