#!/bin/python

# This script is used to process collision data between a given range of GPS coordinates into a heatmap as a dict containing a range of locations as key and a dict of probabilities of collision as value, and export that data to a JSON file that will be used for the game
from extract_mod import extract
import json

path = "C:/DataDive/Transportation/NYC General Transport/NYC-vehicle-collisions.csv"
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
bad_driving = dict(zip(["count"] + bad_driving_reasons, [0] * (len(bad_driving_reasons) + 1)))
driver_condition_reasons = ["FATIGUED/DROWSY", "LOST CONSCIOUSNESS", "PRESCRIPTION MEDICATION", "ALCOHOL INVOLVEMENT", "PHYSICAL DISABILITY", "ILLNESS", "FELL ASLEEP", "DRUGS (ILLEGAL)"]
driver_condition = dict(zip(["count"] + driver_condition_reasons, [0] * (len(driver_condition_reasons) + 1)))
road_condition_reasons = ["PAVEMENT SLIPPERY", "OBSTRUCTION/DEBRIS", "PAVEMENT DEFECTIVE", "LANE MARKING IMPROPER/INADEQUATE", "TRAFFIC CONTROL DEVICE IMPROPER/NON-WORKING", "SHOULDERS DEFECTIVE/IMPROPER"]
road_condition = dict(zip(["count"] + road_condition_reasons, [0] * (len(road_condition_reasons) + 1)))
car_failure_reasons = ["BRAKES DEFECTIVE", "STEERING FAILURE", "TIRE FAILURE/INADEQUATE", "ACCELERATOR DEFECTIVE", "OTHER LIGHTING DEFECTS", "TOW HITCH DEFECTIVE", "HEADLIGHTS DEFECTIVE", "WINDSHIELD INADEQUATE"]
car_failure = dict(zip(["count"] + car_failure_reasons, [0] * (len(car_failure_reasons) + 1)))
bad_luck_reasons = ["OTHER VEHICULAR", "OVERSIZED VEHICLE", "VIEW OBSTRUCTED/LIMITED", "GLARE", "PEDESTRIAN/BICYCLIST/OTHER PEDESTRIAN ERROR/CONFUSION", "DRIVERLESS/RUNAWAY VEHICLE"]
bad_luck = dict(zip(["count"] + bad_luck_reasons, [0] * (len(bad_luck_reasons) + 1)))
collision_prob = dict(zip(["total", "BAD DRIVING", "DRIVER IMPAIRED", "BAD ROAD CONDITION", "CAR FAILURE", "BAD LUCK/SOMEONE ELSE'S FAULT"], [0, bad_driving, driver_condition, road_condition, car_failure, bad_luck])) # A collision dict that will populate the heatmap

for collision in collisions:
	lon = collision["LONGITUDE"]
	if lon != '':
		lon = float(lon)
		lat = float(collision["LATITUDE"])
		if lon > min_long and lon < (min_long + coords_range) and lat > min_lat and lat < (min_lat + coords_range) :
			collision_list.append(dict(zip(["LATITUDE", "LONGITUDE", "FACTOR"], [lon, lat, collision["VEHICLE 1 FACTOR"]])))

# In this part, the collisions will be processed end up with the "heatmap" dict
for collision in collision_list:
	lon = round((collision["LONGITUDE"] // resolution) * resolution, 3)
	lat = round((collision["LATITUDE"] // resolution) * resolution, 3)
	key = str(lon) + ", " + str(lat)
	if key not in heatmap:
		heatmap.append
	else:
		heatmap[key]["total"] += 1
		for reasons in [bad_driving.keys(), driver_condition.keys(), road_condition.keys(), car_failure.keys(), bad_luck.keys()]:
			if collision["FACTOR"] in reasons:
				# reasons[]
				print("it works")
		# heatmap[key][]
