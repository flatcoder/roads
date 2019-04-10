from flask import request, jsonify
from flask_restful import Resource
from app.models import Region, Authority, RoadCategory, Road, Junction, JunctionLink, TrafficCount
import json

class TrafficAPI(Resource):
    def __init__(self):
        self.model = None
        self.set_model()

    def get(self):
        results = self.model.query.all() # iterable if 1
        return self.model.serialize_list(results)#jsonify(list(map(lambda x: x.to_dict(), results)))

    def set_model(self):
        raise NotImplementedError("API base class, derive and implement set_model.")


class RegionsAPI(TrafficAPI):
    def set_model(self):
        self.model = Region

class AuthoritiesAPI(TrafficAPI):
    def set_model(self):
        self.model = Authority

class RoadCategoriesAPI(TrafficAPI):
    def set_model(self):
        self.model = RoadCategory

class RoadsAPI(TrafficAPI):
    def set_model(self):
	    self.model = Road

class JunctionsAPI(TrafficAPI):
    def set_model(self):
        self.model = Junction

class LinksAPI(TrafficAPI):
    def set_model(self):
        self.model = JunctionLink

class CountsAPI(TrafficAPI):
    def set_model(self):
        self.model = TrafficCount

