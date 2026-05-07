from flask import Blueprint, jsonify, request
from pymongo import MongoClient

constructorStandingsMongo = Blueprint("constructorStandingsMongo", __name__)
mongo_constructors = MongoClient("mongodb://mongo_constructors:27017")["constructors_db"]

# GET all constructorStandings
@constructorStandingsMongo.route("/mongo/constructorStandings", methods=["GET"])
def get_all_standings_mongo():
    try:
        standings = list(mongo_constructors["constructorStandings"].find({}, {"_id": 0}))
        return jsonify(standings)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET constructorStanding by id
@constructorStandingsMongo.route("/mongo/constructorStandings/<int:id>", methods=["GET"])
def get_standing_by_id_mongo(id):
    try:
        standing = mongo_constructors["constructorStandings"].find_one({"id": id}, {"_id": 0})
        if standing:
            return jsonify(standing)
        return jsonify({"error": "Standing not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT constructorStandings
@constructorStandingsMongo.route("/mongo/constructorStandings/count", methods=["GET"])
def count_standings():
    try:
        count = mongo_constructors["constructorStandings"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
