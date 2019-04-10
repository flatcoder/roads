from flask import Flask, request
from flask_restful import Api
from app.config import app_config

def create_app(env_name, db):
    from app.api import RegionsAPI, AuthoritiesAPI, RoadCategoriesAPI, \
         RoadsAPI, JunctionsAPI, LinksAPI, CountsAPI

    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    api = Api(app)
    api.add_resource(RegionsAPI, '/regions')
    api.add_resource(AuthoritiesAPI, '/authorities')
    api.add_resource(RoadCategoriesAPI, '/categories')
    api.add_resource(RoadsAPI, '/roads')
    api.add_resource(JunctionsAPI, '/junctions')
    api.add_resource(LinksAPI, '/links')
    api.add_resource(CountsAPI, '/counts')
    db.init_app(app)
    return app
