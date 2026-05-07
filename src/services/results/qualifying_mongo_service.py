from flask import Blueprint, jsonify, request
from pymongo import MongoClient

qualifyingMongo = Blueprint("qualifyingMongo", __name__)
mongo_results = MongoClient("mongodb://mongo_results:27017")["results_db"]

# GET all qualifying
@qualifyingMongo.route("/mongo/qualifying", methods=["GET"])
def get_all_qualifying_mongo():
    try:
        qualifying = list(mongo_results["qualifying"].find({}, {"_id": 0}))
        return jsonify(qualifying)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET qualifying by id
@qualifyingMongo.route("/mongo/qualifying/<int:id>", methods=["GET"])
def get_qualifying_by_id_mongo(id):
    try:
        qualifying = mongo_results["qualifying"].find_one({"id": id}, {"_id": 0})
        if qualifying:
            return jsonify(qualifying)
        return jsonify({"error": "Qualifying not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT qualifying
@qualifyingMongo.route("/mongo/qualifying/count", methods=["GET"])
def count_qualifying():
    try:
        count = mongo_results["qualifying"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
