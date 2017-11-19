#!/bin/python

# Script to generate a heatmap of the collisions using the matplotlib libraries 
from extract_mod import extract
import numpy as np
import numpy.random
import matplotlib.pyplot as plt

path = "C:/DataDive/Transportation/NYC General Transport/NYC-vehicle-collisions.csv"
collisions = extract(path, selected_columns=[5, 6])
# collisions is a list of dicts containing the lon and lat as values from the keys "LONGITUDE" and "LATITUDE", respectively

x = []
y = []

# min_long = -74.2530308
# min_lat = 40.50000251

for collision in collisions:
	# We need to generate the lists of x and y from the collisions list, getting rid of the data outside our range of interest
	if collision["LONGITUDE"] != '':
		if float(collision["LONGITUDE"]) > -80 and float(collision["LONGITUDE"]) < -70:
			x.append(float(collision["LONGITUDE"]))
			y.append(float(collision["LATITUDE"]))

heatmap, xedges, yedges = np.histogram2d(x, y, bins=(55,42))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.savefig("hist.png")