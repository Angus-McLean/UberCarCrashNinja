import numpy as np
import numpy.random
import matplotlib.pyplot as plt
from extract_mod import extract

def map_heat(x, y):
    """Receives two lists of values and makes a heatmap of the value pairs"""
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=100)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()
