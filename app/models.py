from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy_utils import aggregated

db = SQLAlchemy()

class ModelABC(object):
	# 1st PK that's integer and not FK is autoincrement (Serial in postgres).
    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        """ Basic, but enough for now """
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @classmethod
    def get(cls):
        """ Class method means read-only no instance, perfect... """
        try:
            return cls.query.all()
        except:
            raise NotImplementedError("Model base class, derive and implement 'get'.")

    @staticmethod
    def serialize_list(l):
        """ Static method, read-only, no instance, no class... """
        return [m.serialize() for m in l]

class Region(ModelABC, db.Model):
    __tablename__ = 'regions'
    name = db.Column(db.String(80), unique=True, nullable=False)

    @classmethod
    def find_or_create(cls, name):
        rec = cls.query.filter_by(name=name).first()
        if rec == None:
            print("Creating region '"+name+"'.")
            newreg = Region(name=name)
            db.session.add(newreg)
            db.session.commit()
            return newreg
        else:
            # print("Exists with an ID of "+str(rec.id))
            return rec

class Authority(ModelABC, db.Model):
    __tablename__ = 'authorities'

    __table_args__ = (
        db.UniqueConstraint('name', 'region', name='unique_authority_region_combo'),
    )

    name = db.Column(db.String(80), nullable=False)
    region = db.Column(db.Integer, db.ForeignKey('regions.id'))

    @classmethod
    def find_or_create(cls, name, region):
        rec = cls.query.filter_by(name=name, region=region).first()
        if rec == None:
            print("Creating Authority '"+name+"'.")
            newauth = Authority(name=name,region=region)
            db.session.add(newauth)
            db.session.commit()
            return newauth
        else:
            return rec

class RoadCategory(ModelABC, db.Model):
    __tablename__ = 'road_categories'

    code = db.Column(db.String(8), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=False, default="")

    @classmethod
    def find_or_create(cls, code, description):
        rec = cls.query.filter_by(code=code).first()
        if rec == None:
            print("Creating Road Category '"+code+"'.")
            newcat = RoadCategory(code=code,description="")
            db.session.add(newcat)
            db.session.commit()
            return newcat
        else:
            return rec

class Road(ModelABC, db.Model):
    __tablename__ = 'roads'

    name = db.Column(db.String(32), unique=True, nullable=False)

    @classmethod
    def find_or_create(cls, name):
        rec = cls.query.filter_by(name=name).first()
        if rec == None:
            print("Creating Road '"+name+"'.")
            newroad = Road(name=name)
            db.session.add(newroad)
            db.session.commit()
            return newroad
        else:
            return rec

class Junction(ModelABC, db.Model):
    __tablename__ = 'junctions'

    __table_args__ = (
        db.UniqueConstraint('road', 'name', name='unique_road_name_combo'),
    )

    name = db.Column(db.String(80), nullable=False)
    road = db.Column(db.Integer, db.ForeignKey('roads.id'))

    @classmethod
    def find_or_create(cls, name, road):
        rec = cls.query.filter_by(name=name,road=road).first()
        if rec == None:
            print("Creating Junction '"+name+"'.")
            newjun = Junction(name=name,road=road)
            db.session.add(newjun)
            db.session.commit()
            return newjun
        else:
            return rec

class JunctionLink(ModelABC, db.Model):
    __tablename__ = 'links'

    cp = db.Column(db.Integer, nullable=False, unique=True)
    start_junction = db.Column(db.Integer, db.ForeignKey('junctions.id'))
    end_junction = db.Column(db.Integer, db.ForeignKey('junctions.id'))
    road_category = db.Column(db.Integer, db.ForeignKey('road_categories.id'))
    local_authority = db.Column(db.Integer, db.ForeignKey('authorities.id'))

    @classmethod
    def find_or_create(cls, start_junction, end_junction, road_category, local_authority, cp):
        # Might seem overkill, but consider 2 roads that run from the same A to B...
        rec = cls.query.filter_by(cp=cp).first()
        if rec == None:
            print("Creating Junction Link '"+str(start_junction)+"' to '"+str(end_junction)+"'.")
            newlink = JunctionLink(start_junction=start_junction, end_junction=end_junction,
                                   road_category=road_category, local_authority=local_authority, cp=cp)
            db.session.add(newlink)
            db.session.commit()
            return newlink
        else:
            return rec

class TrafficCount(ModelABC, db.Model):
    __tablename__ = 'traffic_counts'

    __table_args__ = (
        db.UniqueConstraint('year', 'link', name='year_link_combo'),
    )

    link = db.Column(db.Integer, db.ForeignKey('links.id'))
    year = db.Column(db.Integer, nullable=False)
    estimated = db.Column(db.Boolean, nullable=False, default=False)
    northing = db.Column(db.Integer, nullable=False)
    easting = db.Column(db.Integer, nullable=False)

    # did debate putting length in junction links, but presume length can actually change
    length_km = db.Column(db.Float, nullable=False, default=0.0)

    pedal_cycles = db.Column(db.Integer, nullable=False, default=0)
    motor_cycles = db.Column(db.Integer, nullable=False, default=0)
    cars_taxis = db.Column(db.Integer, nullable=False, default=0)
    buses_coaches = db.Column(db.Integer, nullable=False, default=0)
    light_goods = db.Column(db.Integer, nullable=False, default=0)
    v2_rigid_hgv = db.Column(db.Integer, nullable=False, default=0)
    v3_rigid_hgv = db.Column(db.Integer, nullable=False, default=0)
    v4_rigid_hgv = db.Column(db.Integer, nullable=False, default=0)
    v4_artic_hgv = db.Column(db.Integer, nullable=False, default=0)
    v5_artic_hgv = db.Column(db.Integer, nullable=False, default=0)
    v6_artic_hgv = db.Column(db.Integer, nullable=False, default=0)

    total_hgv = db.Column(db.Integer, nullable=False, default=0)
    total_all = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def create_from_dict(cls, newcount):
        total_hgv = newcount["v2_rigid_hgv"]+newcount["v3_rigid_hgv"]+newcount["v4_rigid_hgv"]+ \
                    newcount["v4_artic_hgv"]+newcount["v5_artic_hgv"]+newcount["v6_artic_hgv"]
        total_all = total_hgv+newcount["pedal_cycles"]+newcount["motor_cycles"]+ \
                    newcount["cars_taxis"]+newcount["buses_coaches"]+newcount["light_goods"]

        newco = TrafficCount(
                        link=newcount["link"],
                        year=newcount["year"],
                        estimated=newcount["estimated"],
                        easting=newcount["easting"],northing=newcount["northing"],
                        length_km=newcount["length_km"],
                        pedal_cycles=newcount["pedal_cycles"],
                        motor_cycles=newcount["motor_cycles"],
                        cars_taxis=newcount["cars_taxis"],
                        buses_coaches=newcount["buses_coaches"],
                        light_goods=newcount["light_goods"],
                        v2_rigid_hgv=newcount["v2_rigid_hgv"],
                        v3_rigid_hgv=newcount["v3_rigid_hgv"],
                        v4_rigid_hgv=newcount["v4_rigid_hgv"],
                        v4_artic_hgv=newcount["v4_artic_hgv"],
                        v5_artic_hgv=newcount["v5_artic_hgv"],
                        v6_artic_hgv=newcount["v6_artic_hgv"],
                        total_hgv=total_hgv,
                        total_all=total_all
                    )
        try:
            db.session.add(newco)
            db.session.commit()
            return newco
        except:
            return None
