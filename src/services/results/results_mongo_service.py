from flask import Blueprint, jsonify, request
from pymongo import MongoClient

resultsMongo = Blueprint("resultsMongo", __name__)
mongo_results = MongoClient("mongodb://mongo_results:27017")["results_db"]

# GET all results
@resultsMongo.route("/mongo/results", methods=["GET"])
def get_all_results_mongo():
    try:
        results = list(mongo_results["results"].find({}, {"_id": 0}))
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET result by id
@resultsMongo.route("/mongo/results/<int:id>", methods=["GET"])
def get_result_by_id_mongo(id):
    try:
        result = mongo_results["results"].find_one({"id": id}, {"_id": 0})
        if result:
            return jsonify(result)
        return jsonify({"error": "Result not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT results
@resultsMongo.route("/mongo/results/count", methods=["GET"])
def count_results():
    try:
        count = mongo_results["results"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
