from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)

    from .races.races_service import selectOne
    from .races.races_mongo_service import racesMongo

    from .drivers.drivers_service import driversMysql
    from .drivers.driver_mongo_service import driversMongo
    from .drivers.driver_standing_service import driverStandingMysql
    from .drivers.driver_mongo_standings import driverStandingsMongo

    from .constructors.constructor_services import constructorsMysql
    from .constructors.constructor_mongo_services import constructorsMongo
    from .constructors.standings_service import constructorStandingMysql

    app.register_blueprint(selectOne)
    app.register_blueprint(racesMongo)

    app.register_blueprint(driversMysql)
    app.register_blueprint(driversMongo)
    app.register_blueprint(driverStandingMysql)
    app.register_blueprint(driverStandingsMongo)


    app.register_blueprint(constructorsMysql)
    app.register_blueprint(constructorsMongo)
    app.register_blueprint(constructorStandingMysql)
    

    return app


