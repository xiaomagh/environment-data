"""
This file provides the recipe of commands to generate a map projection
with plotted data. Operational code should be modular and all commands
in functions.
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

nc = Dataset('<path>/class5/ostia.nc')
var = nc.variables['analysed_sst']
lons = nc.variables['lon'][::20]  # or whatever the keys are
lats = nc.variables['lat'][::20]
slice2d = var[0,::20,::20]     # for example, to get a 2D slice

m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20)  # whatever map you want

# Convert co-ords to 2D grids of data
X,Y = np.meshgrid(lons, lats)
# Convert from lat-lon to map co-ordinate system
x,y = m(X,Y)

# Use the map co-ordinates and data to create the plot
pc = m.contourf(x, y, slice2d, 30)

plt.colorbar(pc, orientation='horizontal')
m.drawmapboundary()
m.drawcoastlines()
plt.show()
