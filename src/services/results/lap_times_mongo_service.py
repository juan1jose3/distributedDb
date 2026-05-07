from flask import Blueprint, jsonify, request
from pymongo import MongoClient

lapTimesMongo = Blueprint("lapTimesMongo", __name__)
mongo_results = MongoClient("mongodb://mongo_results:27017")["results_db"]

# GET all lapTimes
@lapTimesMongo.route("/mongo/lapTimes", methods=["GET"])
def get_all_lap_times_mongo():
    try:
        lap_times = list(mongo_results["lapTimes"].find({}, {"_id": 0}))
        return jsonify(lap_times)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET lapTime by id
@lapTimesMongo.route("/mongo/lapTimes/<int:id>", methods=["GET"])
def get_lap_time_by_id_mongo(id):
    try:
        lap_time = mongo_results["lapTimes"].find_one({"id": id}, {"_id": 0})
        if lap_time:
            return jsonify(lap_time)
        return jsonify({"error": "Lap time not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT lapTimes
@lapTimesMongo.route("/mongo/lapTimes/count", methods=["GET"])
def count_lap_times():
    try:
        count = mongo_results["lapTimes"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
