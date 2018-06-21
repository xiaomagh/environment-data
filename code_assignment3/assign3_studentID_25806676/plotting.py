""" Contains code for displaying data """

import matplotlib.pyplot as plt
import netcdf_utils
import numpy as np
import netCDF4 as nc
import matplotlib.dates as mdates

def display_map_plot(data, lons, lats, title):
    """
    This function will create and display a map plot. It takes 4 mandatory arguments:
    data: a 2D array of data
    lons: a 1D array of longitude values
    lats: a 1D array of latitude values
    title: a string that is used as the title

    It uses contourf to produce the contour plot
    This plots using 20 different levels/colours - the min and max values are taken from the array automatically.
    """

    pc = plt.contourf(lons, lats, data, 20)
    plt.colorbar(pc, orientation='horizontal')
    plt.title(title)
    plt.xlabel("longitude (degrees east)")
    plt.ylabel("latitude (degrees north)")
    plt.show()
    
    
def display_vertical_plot(data, coor_z, coor_x, title):
    """
    This function will display a vertical profile plot.
    :param data: the data which need to be plotted
    :param coor_z: the vertical coordinate values of the data
    :param coor_x: the x-direction coordinate values of the data
    :param title: a string that is used as the title
    """
    # Get the name of x-label and y-label
    x_label = netcdf_utils.get_title(coor_x)
    y_label = netcdf_utils.get_title(coor_z) 
    
    # Plot the graph
    x,y = np.meshgrid(coor_x, coor_z)
    plt.pcolormesh(x, y, data)
    # Check whether the vertical axis values increase downward
    if netcdf_utils.isPositiveUp(coor_z) == False:
        # Reverse the coordinate data
        plt.gca().invert_yaxis()
    plt.colorbar()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
 

def display_timeseries_plot(data, data_var, coor_t, title):
    """
    This function will display a timeseries plot.
    :param data: the data which need to be plotted
    :param data_var: the variable object of data which contains the information
    :param t_var: the time dimension values
    :param title: a string that is used as the title
    """
    # Get the name of x-label and y-label
    x_label = netcdf_utils.get_title(coor_t)
    y_label = netcdf_utils.get_title(data_var)
    
    # Read the time values from the time dimension values
    time_vals = coor_t[:]
    # Convert the time values to datetime objects
    the_times = []
    the_times = nc.num2date(time_vals, coor_t.units, coor_t.calendar)
    # set up the datetime information for the plot
    day_locator = mdates.DayLocator()
    hour_locator = mdates.HourLocator()
    date_fmt = mdates.DateFormatter('%Y-%m-%d')
    
    # Plot the graph
    plt.plot(the_times, data, color = 'blue',linewidth = 2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    
    # format the ticks
    ax = plt.gca()
    ax.xaxis.set_major_locator(day_locator)
    ax.xaxis.set_major_formatter(date_fmt)
    ax.xaxis.set_minor_locator(hour_locator)
    
    plt.show()
    
    
    