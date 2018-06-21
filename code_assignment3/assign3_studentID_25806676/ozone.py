import matplotlib.pyplot as plt
import numpy as np
import globmodel
from mpl_toolkits.basemap import Basemap

def plot_difference(globmodel_file, sciamachy_file):
    """
    This function extracts data from the SCIAMACHY file, then extracts the 
    corresponding ozone values from the GlobModel file. Calculates the difference 
    between these two kinds of measurements.Then plots the differences as a 
    scatter plot.
    :param globmodel_file: The name of the NetCDF file containing GlobModel data
    :param sciamachy_file: The name of the CSV file containing SCIAMACHY data
    :return: no return
    """
    # Read ozone data from the sciamachy file
    r = np.recfromcsv(sciamachy_file)
    sciamchy_data = r.o3_du
    
    # Extract the ozone data loates on the same location from globmodel file
    globmodel_data = globmodel.read_globmodel(globmodel_file, r.lon, r.lat)
    
    # Calculate the difference between there two measurements
    # Latitude and longitude have the same length-scale
    n = len(r.lat)
    ozone_diff = np.zeros(n)
    for i in range(n):
        ozone_diff[i] = sciamchy_data[i] - globmodel_data[i]
    
    vmax = max(np.abs(ozone_diff))
    
    # Plottitn the scatter plot for this difference
    plt.figure()
    # Make the colorbar centered on zero
    plt.scatter(r.lon, r.lat, c = ozone_diff, cmap='seismic',edgecolors='none'\
                ,vmin=-vmax,vmax = vmax)
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.title('The ozone measurements difference between sciamachy and globmodel results')
    plt.colorbar(extend='both')
    plt.show()
    

def plot_difference_basemap(globmodel_file, sciamachy_file, projection):
    """
    This function extracts data from the SCIAMACHY file, then extracts the 
    corresponding ozone values from the GlobModel file. Calculates the difference 
    between these two kinds of measurements.Then plots the differences using Basemap.
    :param globmodel_file: The name of the NetCDF file containing GlobModel data
    :param sciamachy_file: The name of the CSV file containing SCIAMACHY data
    :param projection: The map projection for using 
    :return: no return
    """
    # Read ozone data from the sciamachy file
    r = np.recfromcsv(sciamachy_file)
    sciamchy_data = r.o3_du
    
    # Extract the ozone data loates on the same location from globmodel file
    globmodel_data = globmodel.read_globmodel(globmodel_file, r.lon, r.lat)
    
    # Calculate the difference between there two measurements
    # Latitude and longitude arrays from satellite have the same lenth-scale
    n = len(r.lat)
    ozone_diff = np.zeros(n)
    for i in range(n):
        ozone_diff[i] = sciamchy_data[i] - globmodel_data[i]
    
    # Determine the projection
    if (projection == 'npstere'):
        m = Basemap(projection='npstere',boundinglat=0.,lon_0=0.)
        m.drawcoastlines()
        # draw parallels and meridians.
        m.drawparallels(np.arange(-80.,81.,20.))
        m.drawmeridians(np.arange(0.,360.,20.))
    elif (projection == 'spstere'):
        m = Basemap(projection='spstere',boundinglat=0.,lon_0=0.)
        m.drawcoastlines()
        # draw parallels and meridians.
        m.drawparallels(np.arange(-80.,81.,20.))
        m.drawmeridians(np.arange(0.,360.,20.))
    elif (projection == 'cyl'):
        m = Basemap(projection='cyl',llcrnrlat=-90.,urcrnrlat=90.,\
                    llcrnrlon=0,urcrnrlon=360)
        m.drawcoastlines()
        # draw parallels and meridians.
        m.drawparallels(np.arange(-80.,81.,20.))
        m.drawmeridians(np.arange(0.,360.,20.))
    else:
        raise ValueError('Try other projections')
    
    # Convert the coordinate variables
    x, y = m(r.lon, r.lat)
    vmax = max(np.abs(ozone_diff))
    m.scatter(x, y, c=ozone_diff, cmap='seismic', edgecolors='none',
              vmin=-vmax, vmax=vmax)
    m.colorbar()
    plt.title('Measurements difference on the projection %s!' % projection) 
    plt.show()
          
        
