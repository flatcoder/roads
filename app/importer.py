from flask_script import Command, Option
from app.models import Region, Authority, Road, RoadCategory, Junction, JunctionLink, TrafficCount
import csv

# Really simple CSV import to get going...
class ImportCommand(Command):
    "Imports CP format CSV"

    option_list = (
        Option('--csv', '-c', dest='csvf'),
    )

    def run(self, csvf):
        if csvf == None:
            print("No input file specified. Use -? for help.")
            return False

        print("Importing "+csvf+"...")
        row = 1
        with open(csvf, "r") as f:
            reader = csv.reader(f, delimiter=",")
            for i, line in enumerate(reader):
                if len(line) != 27:
                    raise Exception("Data not in correct format on row "+str(row)+".")
                elif row != 1:
                    region_name = line[4]
                    region_obj = Region.find_or_create(region_name)
                    region_id = region_obj.id

                    authority_name = line[5]
                    authority_obj = Authority.find_or_create(authority_name, region_id)
                    authority_id = authority_obj.id

                    road_name = line[6]
                    road_obj = Road.find_or_create(road_name)
                    road_id = road_obj.id

                    road_cat = line[7]
                    road_cat_obj = RoadCategory.find_or_create(road_cat,"")
                    road_cat_id = road_cat_obj.id


                    lhs = None
                    rhs = None
                    for p in range(2):
                        junction_name = line[10+p]
                        junction_obj = Junction.find_or_create(junction_name, road_id)
                        junction_id = junction_obj.id

                        if p < 1:
                            lhs = junction_id
                        else:
                            rhs = junction_id

                    cp = int(line[1])
                    link_id = self.create_link(lhs,rhs,road_cat_id,authority_id,cp)
                    self.create_counts(link_id, line, row)
                row = row + 1

    def create_link(self, lhs, rhs, road_cat_id, authority_id,cp):
        if lhs != None and rhs != None:
            # print("We have a right pair here... no really, it's correct.")
            link_obj = JunctionLink.find_or_create(lhs, rhs, road_cat_id, authority_id,cp)
            # print(link_obj)
            return link_obj.id
        else:
            raise Exception("Junction missing on row "+str(row)+".")

    def create_counts(self, link_id, line, row):
        newcount = {}
        newcount["year"] = int(line[0])
        #newcount["cp"] = int(line[1])
        newcount["estimated"] = True
        if line[2] == "Counted":
            newcount["estimated"] = False
        newcount["link"] = link_id
        newcount["easting"] = int(line[8])
        newcount["northing"] = int(line[9])
        newcount["length_km"] = float(line[12])
        newcount["pedal_cycles"] = int(line[14])
        newcount["motor_cycles"] = int(line[15])
        newcount["cars_taxis"] = int(line[16])
        newcount["buses_coaches"] = int(line[17])
        newcount["light_goods"] =  int(line[18])
        newcount["v2_rigid_hgv"] = int(line[19])
        newcount["v3_rigid_hgv"] = int(line[20])
        newcount["v4_rigid_hgv"] = int(line[21])
        newcount["v4_artic_hgv"] = int(line[22])
        newcount["v5_artic_hgv"] = int(line[23])
        newcount["v6_artic_hgv"] = int(line[24])
        # 25 = ALL HGV, 26 = ALL VEHICLE
        # and insert
        newc = TrafficCount.create_from_dict(newcount)
        if newc == None:
            raise Exception("Error importing row "+str(row)+".")

