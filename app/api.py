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
        link_id = 0

        # Filter on a specific CP (junction pair)
        if "cp" in request.args:
            cp = int(request.args["cp"])
            lnk = JunctionLink.query.filter_by(cp=cp).first()
            if lnk != None:
                link_id = lnk.id

        # Order by length, total asc or desc
        """if "order_by" in request.args:
            if "order" in request.args:
                if request.args["order"] == "desc":
                    if request.args["order_by"] == "length":
                        if link_id > 0:
                            newq = self.model.query.filter_by(link=link_id).order_by(TrafficCount.length_km.desc())
                        else:
                            newq = self.model.query.filter().order_by(TrafficCount.length_km.desc())
                    else:
                        if link_id > 0:
                            newq = self.model.query.filter_by(link=link_id).order_by(TrafficCount.total_all.desc())
                        else:
                            newq = self.model.query.filter().order_by(TrafficCount.total_all.desc())

            if request.args["order_by"] == "length" and newq == None:
                if link_id > 0:
                    newq = self.model.query.filter_by(link=link_id).order_by(TrafficCount.length_km.asc())
                else:
                    newq = self.model.query.filter().order_by(TrafficCount.length_km.asc())
            elif newq == None:
                if link_id > 0:
                    newq = self.model.query.filter_by(link=link_id).order_by(TrafficCount.total_all.asc())
                else:
                    newq = self.model.query.filter().order_by(TrafficCount.total_all.asc())"""

        # Limits and offsets
        if perpage > 0:
            # Order applied?
            if newq == None:
                return self.model.query.limit(perpage).offset(page*perpage)
            else:
                return newq.limit(perpage).offset(page*perpage)

        # Order applied?
        if newq != None:
            if link_id > 0:
                return newq.filter_by(link=link_id)
            return newq.all()

        # CP set?
        if link_id > 0:
            return self.model.query.filter_by(link=link_id)
        return self.model.query.all()
