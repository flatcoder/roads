from flask import request, jsonify
from flask_restful import Resource
from app.models import Region, Authority, RoadCategory, Road, Junction, JunctionLink, TrafficCount
import json

class TrafficAPI(Resource):
    def __init__(self):
        self.model = None
        self._set_model()

    def get(self):
        #print(request.args)
        results = []
        perpage = 0
        page = 0

        if "perpage" in request.args:
            perpage = int(request.args["perpage"])

        if "page" in request.args:
            page = int(request.args["page"])

        results = self._search_filter_order(request, perpage, page)
        return self.model.serialize_list(results)

    def _search_filter_order(self, request, perpage, page):
        if perpage > 0:
            return self.model.query.limit(perpage).offset(page*perpage)
        return self.model.query.all()

    def _set_model(self):
        raise NotImplementedError("API base class, derive and implement _set_model.")

class RegionsAPI(TrafficAPI):
    def _set_model(self):
        self.model = Region

class AuthoritiesAPI(TrafficAPI):
    def _set_model(self):
        self.model = Authority

class RoadCategoriesAPI(TrafficAPI):
    def _set_model(self):
        self.model = RoadCategory

class RoadsAPI(TrafficAPI):
    def _set_model(self):
	    self.model = Road

class JunctionsAPI(TrafficAPI):
    def _set_model(self):
        self.model = Junction

class LinksAPI(TrafficAPI):
    def _set_model(self):
        self.model = JunctionLink

class CountsAPI(TrafficAPI):
    def _set_model(self):
        self.model = TrafficCount

    def _search_filter_order(self, request, perpage, page):
        newq = None

        if "order_by" in request.args:
            if "order" in request.args:
                if request.args["order"] == "desc":
                    if request.args["order_by"] == "length":
                        newq = self.model.query.filter().order_by(TrafficCount.length_km.desc())
                    else:
                        newq = self.model.query.filter().order_by(TrafficCount.total_all.desc())

            if request.args["order_by"] == "length" and newq == None:
                newq = self.model.query.filter().order_by(TrafficCount.length_km.asc())
            elif newq == None:
                newq = self.model.query.filter().order_by(TrafficCount.total_all.asc())

        if perpage > 0:
            if newq == None:
                return self.model.query.limit(perpage).offset(page*perpage)
            else:
                return newq.limit(perpage).offset(page*perpage)

        if newq != None:
            return newq.filter()

        # default
        return self.model.query.filter()

"""        lhs = 0
        rhs = 0
        road = 0

        if "lhs_junction" in request.args:
            lhs = int(request.args["lhs_junction"])

        if "rhs_junction" in request.args:
            rhs = int(request.args["rhs_junction"])

        if "road" in request.args:
            road = int(request.args["road"])
"""

