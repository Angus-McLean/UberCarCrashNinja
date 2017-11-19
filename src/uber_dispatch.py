#!/bin/python

from extract_mod import extract
from random import choice

class Uber_Dispatch():
    """A Uber dispatcher that can send coordinates for a pick up"""
    

    def __init__(self, base, data_file):
        """Constructor, takes the dispatch base and a file of uber data"""
        self.pickup_loc = {"Lat": 0.0, "Lon": 0.0}
        self.base = base

        data = extract(data_file, selected_columns=[3, 1, 2])
        self.locations = []
        loc = {}
        for row in data:
            if row["Base"] == base:
                loc["Lat"] = row["Lat"]
                loc["Lon"] = row["Lon"]
                self.locations.append(loc.copy())
            loc.clear()

    def set_pickup(self):
        """Sets a pickup location at random from the possible places for that dispatch"""
        self.pickup_loc = choice(self.locations)

    def get_lat(self):
        """Getter for the latitude of the pickup location"""
        return float(self.pickup_loc["Lat"])

    def get_lon(self):
        """Getter for the longitude of the pickup location"""
        return float(self.pickup_loc["Lon"])
