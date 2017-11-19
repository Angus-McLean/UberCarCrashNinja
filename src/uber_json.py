#!/bin/python

# Script to turn Uber data in json format
from extract_mod import extract
import json

path = "/home/sam/Documents/DataDive/Transportation/NYC Uber-Taxi Data/NYC Uber - 2014/uber-raw-data-jul14.csv"
pickups = extract(path, selected_columns = [1, 2]) # Corresponds to "Lat", "Lon", respectively

pickup_list = [] # List that will contain all the pickups that are in our range of location
min_long = -74.0125 # x origin
min_lat = 40.65 # y origin
lon = 0.0
lat = 0.0
coords_range = 0.15 # Range of coords
resolution = 0.005 # Resolution of our "grid"
heatmap = {} # The heatmap dicts

# Lists of big reasons, each one of these containing more details as keys, count as values
# bad_driving_reasons = ["DRIVER INATTENTION/DISTRACTION", "FAILURE TO YIELD RIGHT-OF-WAY", "BACKING UNSAFELY", "TURNING IMPROPERLY", "FOLLOWING TOO CLOSELY", "TRAFFIC CONTROL DISREGARDED", "DRIVER INEXPERIENCE", "PASSING OR LANE USAGE IMPROPER", "UNSAFE LANE CHANGING", "OUTSIDE CAR DISTRACTION", "REACTION TO OTHER UNINVOLVED VEHICLE", "UNSAFE SPEED", "PASSENGER DISTRACTION", "AGGRESSIVE DRIVING/ROAD RAGE", "OTHER ELECTRONIC DEVICE", "FAILURE TO KEEP RIGHT", "ANIMALS ACTION", "CELL PHONE (HANDS-FREE)", "CELL PHONE (HAND-HELD)"]
# bad_driving = dict(zip(["count"] + bad_driving_reasons, [0] * (len(bad_driving_reasons) + 1)))
# driver_condition_reasons = ["FATIGUED/DROWSY", "LOST CONSCIOUSNESS", "PRESCRIPTION MEDICATION", "ALCOHOL INVOLVEMENT", "PHYSICAL DISABILITY", "ILLNESS", "FELL ASLEEP", "DRUGS (ILLEGAL)"]
# driver_condition = dict(zip(["count"] + driver_condition_reasons, [0] * (len(driver_condition_reasons) + 1)))
# road_condition_reasons = ["PAVEMENT SLIPPERY", "OBSTRUCTION/DEBRIS", "PAVEMENT DEFECTIVE", "LANE MARKING IMPROPER/INADEQUATE", "TRAFFIC CONTROL DEVICE IMPROPER/NON-WORKING", "SHOULDERS DEFECTIVE/IMPROPER"]
# road_condition = dict(zip(["count"] + road_condition_reasons, [0] * (len(road_condition_reasons) + 1)))
# car_failure_reasons = ["BRAKES DEFECTIVE", "STEERING FAILURE", "TIRE FAILURE/INADEQUATE", "ACCELERATOR DEFECTIVE", "OTHER LIGHTING DEFECTS", "TOW HITCH DEFECTIVE", "HEADLIGHTS DEFECTIVE", "WINDSHIELD INADEQUATE"]
# car_failure = dict(zip(["count"] + car_failure_reasons, [0] * (len(car_failure_reasons) + 1)))
# bad_luck_reasons = ["OTHER VEHICULAR", "OVERSIZED VEHICLE", "VIEW OBSTRUCTED/LIMITED", "GLARE", "PEDESTRIAN/BICYCLIST/OTHER PEDESTRIAN ERROR/CONFUSION", "DRIVERLESS/RUNAWAY VEHICLE"]
# bad_luck = dict(zip(["count"] + bad_luck_reasons, [0] * (len(bad_luck_reasons) + 1)))
# collision_prob = dict(zip(["total", "BAD DRIVING", "DRIVER IMPAIRED", "BAD ROAD CONDITION", "CAR FAILURE", "BAD LUCK/SOMEONE ELSE'S FAULT"], [0, bad_driving, driver_condition, road_condition, car_failure, bad_luck])) # A collision dict that will populate the heatmap

for pickup in pickups:
	lon = pickup["Lon"]
	if lon != '':
		lon = float(lon)
		lat = float(pickup["Lat"])
		if lon > min_long and lon < (min_long + coords_range) and lat > min_lat and lat < (min_lat + coords_range) :
			pickup_list.append([lon, lat])

# In this part, the collisions will be processed end up with the "heatmap" dict
for pickup in pickup_list:
	lon = round((pickup[0] // resolution) * resolution, 3)
	lat = round((pickup[1] // resolution) * resolution, 3)
	key = str(lon) + ", " + str(lat)
	heatmap[key] = heatmap.get(key, 0) + 1

# Making the values held in the dictionary fractions
for coord in heatmap:
    heatmap[coord] = heatmap[coord] / len(pickup_list)

# Writing the heatmap to the JSON file
file_name = "/home/sam/Documents/DataDive/Angus_repo/UberCarCrashNinja/json_files/uber.json"
with open(file_name, 'w') as f:
    json.dump(heatmap, f)
