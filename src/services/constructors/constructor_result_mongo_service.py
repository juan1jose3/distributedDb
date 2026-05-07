from flask import Blueprint, jsonify, request
from pymongo import MongoClient

constructorResultsMongo = Blueprint("constructorResultsMongo", __name__)
mongo_constructors = MongoClient("mongodb://mongo_constructors:27017")["constructors_db"]

# GET all constructorResults
@constructorResultsMongo.route("/mongo/constructorResults", methods=["GET"])
def get_all_results_mongo():
    try:
        results = list(mongo_constructors["constructorResults"].find({}, {"_id": 0}))
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET constructorResult by id
@constructorResultsMongo.route("/mongo/constructorResults/<int:id>", methods=["GET"])
def get_result_by_id_mongo(id):
    try:
        result = mongo_constructors["constructorResults"].find_one({"id": id}, {"_id": 0})
        if result:
            return jsonify(result)
        return jsonify({"error": "Constructor result not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT constructorResults
@constructorResultsMongo.route("/mongo/constructorResults/count", methods=["GET"])
def count_results():
    try:
        count = mongo_constructors["constructorResults"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
