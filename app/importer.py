from flask_script import Command, Option
from app.models import Region, Authority, Road, RoadCategory, Junction, JunctionLink
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

                    link_id = self.create_link(lhs,rhs)
                    self.create_counts(link_id, line)
                row = row + 1

    def create_link(self, lhs, rhs):
        if lhs != None and rhs != None:
            # print("We have a right pair here... no really, it's correct.")
            link_obj = JunctionLink.find_or_create(lhs, rhs, road_cat_id, authority_id)
            # print(link_obj)
            return link_obj.id
        else:
            raise Exception("Junction missing on row "+str(row)+".")

    def create_counts(self, link_id, row):
        year = int(row[0])
        cp = int(row[1])
        estimated = True
        if row[2] == "Counted":
            estimated = False
        easting = int(row[8])
        northing = int(row[9])
        length_km = float(row[12])
        pedal_cycles = int(row[14])
        motor_cycles = int(row[15])
        cars_taxis = int(row[16])
        buses_coaches = int(row[17])
        light_goods =  int(row[18])
        v2_rigid_hgv = int(row[19])
        v3_rigid_hgv = int(row[20])
        v4_rigid_hgv = int(row[21])
        v4_artic_hgv = int(row[22])
        v5_artic_hgv = int(row[23])
        v6_artic_hgv = int(row[24])
        # 25 = ALL HGV, 26 = ALL VEHICLE

        # and insert

