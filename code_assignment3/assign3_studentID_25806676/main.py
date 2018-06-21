import netCDF4
import extract
import plotting
import netcdf_utils
import os

def plot_map(filename, varname, t_index, z_index):
    """
    This function plots a map from NetCDF data.
    The function extracts the relevant data using functions from netcdf_utils and extract
    It plots the data using functions from plotting
    This function also uses the NetCDF4 library.
    There is no extra error handling  - the function will not work if the arguments are incorrect
    The netcdf file must contain a valid latitude and longitude variable
    :param filename: location of a NetCDF file as a string (in file system)
    :param varname: the identifier of the variable that is to be plotted
    :param t_index: index along the time axis as an integer
    :param z_index: index along the vertical axis as an integer
    :return: no return
    """
    nc = netCDF4.Dataset(filename)
    data_var = nc.variables[varname]
    
    # Extract the required data
    data = extract.extract_map_data(nc, data_var, t_index, z_index)
    
    # Find the longitude and latitude values
    lon_var = netcdf_utils.find_longitude_var(nc, data_var)
    lon_vals = lon_var[:]
    lat_var = netcdf_utils.find_latitude_var(nc, data_var)
    lat_vals = lat_var[:]
    
    title = "Plot of %s" % netcdf_utils.get_title(data_var)
    
    plotting.display_map_plot(data, lon_vals, lat_vals, title)
    

def plot_vertical_section(filename, varname, direction, value, t_index):
    """
    This function plots a vertical section from NetCDF data.
    The function extracts the relevant data using functions from netcdf_utils and extract
    It plots the data using functions from plotting
    This function also uses the NetCDF4 library.
    There is no extra error handling  - the function will not work if the arguments are incorrect
    The netcdf file must contain a valid latitude and longitude variable
    :param filename: location of a NetCDF file as a string (in file system)
    :param varname: the identifier of the variable that is to be plotted
    :param direction: the direction of the vertical section as a string
    :param value: the latitude or longitude that section represents
    :param t_index: index along the time axis as an integer
    :return: no return
    """
    nc = netCDF4.Dataset(filename)
    data_var = nc.variables[varname]
      
    # Extract the required vertical profile data and coordinate data
    data, coor_x, coor_z = \
         extract.extract_vertical_data(nc, data_var, direction, value, t_index)

    # Determine the title of the plot
    title = '{direction} section of {name} ({unit}) at {value} degrees {coord}'\
    .format(
    direction=direction,\
    name=netcdf_utils.get_attribute(data_var, 'standard_name', data_var._name),\
    unit=netcdf_utils.get_attribute(data_var, 'units', 'no units'),\
    value=value, coord =('latitude' if direction == 'EW' else 'longitude')\
    )
      
    plotting.display_vertical_plot(data, coor_z, coor_x, title)


def plot_timeseries(filename, varname, lon, lat, z):
    """
    This function plots the time series from NetCDF data.
    The function extracts the relevant data using functions from netcdf_utils and extract
    It plots the data using functions from plotting.
    :param filename: location of a NetCDF file as a string (in file system)
    :param varname: the identifier of the variable that is to be plotted
    :param lon: the value of longitude in degrees
    :param lat: the value of latitude in degrees
    :param z: the value of vertical coordinate variable
    :return: no return
    """
    nc = netCDF4.Dataset(filename)
    data_var = nc.variables[varname]

    # Extract the required data and coordinate data
    data, coor_t = extract.extract_timeseries(nc, data_var, lon, lat, z)
  
    # Determine the title of the plot
    z_var = netcdf_utils.find_vertical_var(nc, data_var)
    if z_var:
        title = 'Time series for {name} ({unit})\nat {lat} degrees latitude and ' \
                '{lon} degrees longitude\n on {z} ({z_unit}) layer'\
                .format(
            name=netcdf_utils.get_attribute(data_var, 'standard_name', data_var._name),
            unit=netcdf_utils.get_attribute(data_var, 'units', 'no units'),
            lat=lat, lon=lon, z=z, \
            z_unit=netcdf_utils.get_attribute(z_var, 'units', 'no units')\
            )
        
        plotting.display_timeseries_plot(data, data_var, coor_t, title)
    
    else:
        title = 'Time series for {name} ({unit})\nat {lat} degrees latitude and ' \
                '{lon} degrees longitude'\
                .format(
            name=netcdf_utils.get_attribute(data_var, 'standard_name', data_var._name),
            unit=netcdf_utils.get_attribute(data_var, 'units', 'no units'),
            lat=lat, lon=lon
            )
        
        plotting.display_timeseries_plot(data, data_var, coor_t, title)


#### Here are some tests
#### Simply run this script to run them.

#if __name__ == '__main__':
#    data_path = os.path.normpath(
#        "C:/Users/xw904346/Documents/05_ReSC/09_SoftwareEngineering in Met/"
#        "05_MTMD01_EnvVis/01_course_material/classes/lecture_03/data/polcoms.nc")
#    plot_map(data_path, "POT", 0, 0)
#
#    data_path = os.path.normpath(
#        "C:/Users/xw904346/Documents/05_ReSC/09_SoftwareEngineering in Met/"
#        "05_MTMD01_EnvVis/01_course_material/classes/lecture_06/data/GlobModel_temp.nc")
#    plot_map(data_path, "ta", 0, 5)
#
#    data_path = os.path.normpath("C:/Users/xw904346\Dropbox\courses\MTMD01_16-17"
#                                 "\Week 05\HadCEM.nc")
#    plot_map(data_path, "salinity", 0, 10)
    # The OSTIA dataset is large, so this test can be slow.  Uncomment
    # these lines to run it
    # data_path = os.path.normpath("<your_path>/ostia.nc")
    # plot_map(data_path, "analysed_sst", 0, 5)
    
