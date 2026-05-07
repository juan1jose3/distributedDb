from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

driverStandingsMongo = Blueprint("driverStandingsMongo", __name__)
mongo_drivers = MongoClient("mongodb://mongo_drivers:27017")["drivers_db"]

# GET all driverStandings
@driverStandingsMongo.route("/mongo/driverStandings", methods=["GET"])
def get_all_standings_mongo():
    try:
        standings = list(mongo_drivers["driverStandings"].find({}, {"_id": 0}))
        return jsonify(standings)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET driverStanding by id
@driverStandingsMongo.route("/mongo/driverStandings/<int:id>", methods=["GET"])
def get_standing_by_id_mongo(id):
    try:
        standing = mongo_drivers["driverStandings"].find_one({"id": id}, {"_id": 0})
        if standing:
            return jsonify(standing)
        return jsonify({"error": "Standing not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT driverStandings
@driverStandingsMongo.route("/mongo/driverStandings/count", methods=["GET"])
def count_standings():
    try:
        count = mongo_drivers["driverStandings"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})