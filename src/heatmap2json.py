#!/bin/python

# This script is used to process collision data between a given range of GPS coordinates into a heatmap as a dict containing a range of locations as key and a dict of probabilities of collision as value, and export that data to a JSON file that will be used for the game
from extract_mod import extract
import json

path = "/home/sam/Documents/DataDive/Transportation/NYC General Transport/NYC-vehicle-collisions.csv"
collisions = extract(path, selected_columns = [5, 6, 24]) # Corresponds to "LATITUDE", "LONGITUDE" and "VEHICLE 1 FACTOR" respectively

collision_list = [] # List that will contain all the collisions that are in our range of location
min_long = -74.0125 # x origin
min_lat = 40.65 # y origin
lon = 0.0
lat = 0.0
coords_range = 0.15 # Range of coords
resolution = 0.005 # Resolution of our "grid"
heatmap = dict() # The heatmap dicts

# Lists of big reasons, each one of these containing more details as keys, count as values
bad_driving_reasons = ["DRIVER INATTENTION/DISTRACTION", "FAILURE TO YIELD RIGHT-OF-WAY", "BACKING UNSAFELY", "TURNING IMPROPERLY", "FOLLOWING TOO CLOSELY", "TRAFFIC CONTROL DISREGARDED", "DRIVER INEXPERIENCE", "PASSING OR LANE USAGE IMPROPER", "UNSAFE LANE CHANGING", "OUTSIDE CAR DISTRACTION", "REACTION TO OTHER UNINVOLVED VEHICLE", "UNSAFE SPEED", "PASSENGER DISTRACTION", "AGGRESSIVE DRIVING/ROAD RAGE", "OTHER ELECTRONIC DEVICE", "FAILURE TO KEEP RIGHT", "ANIMALS ACTION", "CELL PHONE (HANDS-FREE)", "CELL PHONE (HAND-HELD)"]
# bad_driving = dict(zip(["count"] + bad_driving_reasons, [0] * (len(bad_driving_reasons) + 1)))
driver_impaired_reasons = ["FATIGUED/DROWSY", "LOST CONSCIOUSNESS", "PRESCRIPTION MEDICATION", "ALCOHOL INVOLVEMENT", "PHYSICAL DISABILITY", "ILLNESS", "FELL ASLEEP", "DRUGS (ILLEGAL)"]
# driver_impaired = dict(zip(["count"] + driver_impaired_reasons, [0] * (len(driver_impaired_reasons) + 1)))
road_condition_reasons = ["PAVEMENT SLIPPERY", "OBSTRUCTION/DEBRIS", "PAVEMENT DEFECTIVE", "LANE MARKING IMPROPER/INADEQUATE", "TRAFFIC CONTROL DEVICE IMPROPER/NON-WORKING", "SHOULDERS DEFECTIVE/IMPROPER"]
# road_condition = dict(zip(["count"] + road_condition_reasons, [0] * (len(road_condition_reasons) + 1)))
car_failure_reasons = ["BRAKES DEFECTIVE", "STEERING FAILURE", "TIRE FAILURE/INADEQUATE", "ACCELERATOR DEFECTIVE", "OTHER LIGHTING DEFECTS", "TOW HITCH DEFECTIVE", "HEADLIGHTS DEFECTIVE", "WINDSHIELD INADEQUATE"]
# car_failure = dict(zip(["count"] + car_failure_reasons, [0] * (len(car_failure_reasons) + 1)))
bad_luck_reasons = ["OTHER VEHICULAR", "OVERSIZED VEHICLE", "VIEW OBSTRUCTED/LIMITED", "GLARE", "PEDESTRIAN/BICYCLIST/OTHER PEDESTRIAN ERROR/CONFUSION", "DRIVERLESS/RUNAWAY VEHICLE"]
# bad_luck = dict(zip(["count"] + bad_luck_reasons, [0] * (len(bad_luck_reasons) + 1)))
# collision_prob = dict(zip(["total", "BAD DRIVING", "DRIVER IMPAIRED", "BAD ROAD CONDITION", "CAR FAILURE", "BAD LUCK/SOMEONE ELSE'S FAULT"], [0, bad_driving, driver_impaired, road_condition, car_failure, bad_luck])) # A collision dict that will populate the heatmap

reasons = {"Bad Driving": bad_driving_reasons, "Driver Impaired": driver_impaired_reasons, "Road Condition": road_condition_reasons, "Car Failure": car_failure_reasons, "Bad Luck": bad_luck_reasons}
entry_template = {"overall": 0, "Bad Driving": 0, "Driver Impaired": 0, "Road Condition": 0, "Car Failure": 0, "Bad Luck": 0}

for collision in collisions:
    lon = collision["LONGITUDE"]
    if lon != '':
        lon = float(lon)
        lat = float(collision["LATITUDE"])
        if lon > min_long and lon < (min_long + coords_range) and lat > min_lat and lat < (min_lat + coords_range) :
            # Calculating in which "box" the collision takes place, and creating the key out if it for the heatmap
            lon = round((lon // resolution) * resolution, 3)
            lat = round((lat // resolution) * resolution, 3)

            # First, finding in which dict of reasons ("bad_driver", "driver_impaired", ...) the reason of the collision is
            for reason in reasons:
                if collision["VEHICLE 1 FACTOR"] in reasons[reason]:
					# print(collision["VEHICLE 1 FACTOR"] + " is in " + str(big_reason) + " at key '" + str(lat) + ", " + str(lon) + "'")
                    key = str(lat) + ", " + str(lon)
                    heatmap[key] = heatmap.get(key, entry_template.copy())
                    heatmap[key][reason] += 1
                    heatmap[key]["overall"] += 1
			# Now, incrementing the count for that reason and the count of the dict of reasons in which it is
			# collision_list.append(dict(zip(["LATITUDE", "LONGITUDE", "FACTOR"], [lon, lat, collision["VEHICLE 1 FACTOR"]])))
total_crashes = 0
for loc in heatmap:
    total_crashes += heatmap[loc]["overall"]

for loc in heatmap:
    for reason in heatmap[loc]:
        if reason != "overall":
            heatmap[loc][reason] = heatmap[loc][reason] / heatmap[loc]["overall"]
    heatmap[loc]["overall"] = heatmap[loc]["overall"] / total_crashes

file_path = "/home/sam/Documents/DataDive/Angus_repo/UberCarCrashNinja/json_files/crash.json"
with open(file_path, 'w') as f:
    json.dump(heatmap, f)

# In this part, the collisions will be processed end up with the "heatmap" dict
# for collision in collision_list:
# 	key = str(lon) + ", " + str(lat)
# 	# Populating the heatmap with the collisions and counting the number of corresponding event
# 	# If the key doesn't exist, it is added to the dict, with a value being a collision_prob dict with 0s for all the values
# 	if not key in str(heatmap.keys()):
# 		print(key + " is not in the heatmap")
# 		# Reinitializing the dicts
# 		collision_prob["total"] = 1
# 		for key in bad_driving:
# 			bad_driving[key] = 0
# 		for key in driver_impaired:
# 			driver_impaired[key] = 0
# 		for key in road_condition:
# 			road_condition[key] = 0
# 		for key in car_failure:
# 			car_failure[key] = 0
# 		for key in bad_luck:
# 			bad_luck[key] = 0
# 		heatmap[key] = collision_prob.copy()
# 		#fix this
# 	# If the key already exists, we increment the total number of collisions in the "box" corresponding to the key, and we look for the specific reason of the collision in the dicts of collisions reasons to increment its specific counter as well as the counter of collisions in the bigger group of reasons
# 	else:
# 		print(key + " is already in the heatmap")
# 		heatmap[key]["total"] += 1
# 		for reasons in [bad_driving.keys(), driver_impaired.keys(), road_condition.keys(), car_failure.keys(), bad_luck.keys()]:
# 			print(str(reasons))
# 			if collision["FACTOR"] in reasons:
# 				# reasons[]
# 				print("it works")
# 		# heatmap[key][]
