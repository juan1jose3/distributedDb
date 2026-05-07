from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)

    from .races_service import selectOne
    from .races_mongo_service import racesMongo

    app.register_blueprint(selectOne)
    app.register_blueprint(racesMongo)

    return app