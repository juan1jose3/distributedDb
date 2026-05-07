from flask import Blueprint, jsonify, request
from connection import get_connection
from pymongo import MongoClient

driversMongo = Blueprint("driversMongo", __name__)
mongo_drivers = MongoClient("mongodb://mongo_drivers:27017")["drivers_db"]

# GET all drivers
@driversMongo.route("/mongo/drivers", methods=["GET"])
def get_all_mongo():
    try:
        drivers = list(mongo_drivers["drivers"].find({}, {"_id": 0}))
        return jsonify(drivers)
    except Exception as e:
        return jsonify({"error": str(e)})

# GET driver by id
@driversMongo.route("/mongo/drivers/<int:id>", methods=["GET"])
def get_by_id_mongo(id):
    try:
        driver = mongo_drivers["drivers"].find_one({"id": id}, {"_id": 0})
        if driver:
            return jsonify(driver)
        return jsonify({"error": "Driver not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# COUNT drivers
@driversMongo.route("/mongo/drivers/count", methods=["GET"])
def count_drivers():
    try:
        count = mongo_drivers["drivers"].count_documents({})
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)})