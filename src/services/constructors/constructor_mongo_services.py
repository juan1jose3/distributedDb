from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

constructorsMongo = Blueprint("constructorsMongo",__name__)

mongo_constructors = MongoClient("mongodb://mongo_constructors:27017")["constructors_db"]

# GET all constructors
@constructorsMongo.route("/mongo/constructors", methods=["GET"])
def get_all_mongo():
    try:
        constructors = list(mongo_constructors["constructors"].find({}, {"_id": 0}))
        return jsonify(constructors)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET constructor by id
@constructorsMongo.route("/mongo/constructors/<int:id>", methods=["GET"])
def get_by_id_mongo(id):
    try:
        constructor = mongo_constructors["constructors"].find_one({"id": id}, {"_id": 0})
        if constructor:
            return jsonify(constructor)
        return jsonify({"error": "Constructor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT constructors
@constructorsMongo.route("/mongo/constructors/count", methods=["GET"])
def count_constructors():
    try:
        count = mongo_constructors["constructors"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})