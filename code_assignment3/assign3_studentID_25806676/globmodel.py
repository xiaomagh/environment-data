import netCDF4
import netcdf_utils
import numpy as np

def read_globmodel(filename, array_lon, array_lat):
    """
    This function finds out the ozone data from the GlobModel model results which 
    has the same location as the satellite measurements'. And then return the 
    list of the ozone data which is extracted from the GlobModel data.
    :param filename: the name of the NetCDF file containing GlobModel data.
    :param array_lon: An array of longitude coordinate values of the extracted data 
    :param array_lat: An array of latitude coordinate values of the extracted data
    :return: the extracted ozone data from GlobModel results with unit DU
    """
    nc = netCDF4.Dataset(filename)
    data_var = nc.variables['colo3']
    
    # Latitude and longitude arrays from satellite have the same lenth-scale
    n = len(array_lat)
    ozone_value = np.zeros(n)    
    
    # Extract the data on the same location as satellite
    for i in range(n):
        lat_index = netcdf_utils.find_nearest_lat_index(nc, data_var, array_lat[i])
        lon_index = netcdf_utils.find_nearest_lon_index(nc, data_var, array_lon[i])
            
        # The time index of ozone from globmodel should be 0 because its shape is 1
        ozone_value[i] = data_var[0, lat_index, lon_index]/2.1414E-5
    
    
    return ozone_value
    