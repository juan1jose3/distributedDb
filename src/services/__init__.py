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
    from .constructors.standings_mongo_service import constructorStandingsMongo
    from .constructors.constructor_result_service import constructorResultMysql
    from .constructors.constructor_result_mongo_service import constructorResultsMongo

    from .results.results_service import resultsMysql
    from .results.results_mongo_service import resultsMongo
    from .results.qualifying_service import qualifyingMysql
    from .results.qualifying_mongo_service import qualifyingMongo
    from .results.lap_times_service import lapTimesMysql
    from .results.lap_times_mongo_service import lapTimesMongo

    app.register_blueprint(selectOne)
    app.register_blueprint(racesMongo)

    app.register_blueprint(driversMysql)
    app.register_blueprint(driversMongo)
    app.register_blueprint(driverStandingMysql)
    app.register_blueprint(driverStandingsMongo)


    app.register_blueprint(constructorsMysql)
    app.register_blueprint(constructorsMongo)
    app.register_blueprint(constructorStandingMysql)
    app.register_blueprint(constructorStandingsMongo)
    app.register_blueprint(constructorResultMysql)
    app.register_blueprint(constructorResultsMongo)

    app.register_blueprint(resultsMysql)
    app.register_blueprint(resultsMongo)
    app.register_blueprint(qualifyingMysql)
    app.register_blueprint(qualifyingMongo)
    app.register_blueprint(lapTimesMysql)
    app.register_blueprint(lapTimesMongo)
    

    return app


