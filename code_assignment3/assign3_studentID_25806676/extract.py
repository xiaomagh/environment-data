""" Contains code for extracting data from NetCDF files """

import netcdf_utils as nu


def extract_map_data(nc, data_var, t_index, z_index):
    """
    This function extracts data ready to be plotted on a map.  It takes 4 arguments:
    nc: a NetCDF Dataset object
    data_var: a NetCDF Variable object representing the variable to be extracted 
    t_index: the desired index along the time axis (if present) - an integer
    z_index: the desired index along the z-axis (if present) - an integer
    
    The function returns a 2D numpy array of map data
    """

    # Find the number of dimensions for the data variable
    num_dims = len(data_var.dimensions)
    if num_dims < 2 or num_dims > 4:
        # This shows an example of raising an exception if bad input means that we can't proceed further
        raise ValueError("Cannot extract data from variable with %d dimensions" % num_dims)
    
    lon_var = nu.find_longitude_var(nc, data_var)
    lat_var = nu.find_latitude_var(nc, data_var)

    if lon_var is None or lat_var is None:
        raise ValueError("Need both latitude and longitude dimensions to extract map data")

    if num_dims == 2:
        # Simple case - just return all the data
        return data_var[:,:]
    elif num_dims == 3:
        # Determine whether to use time or z axis
        z_var = nu.find_vertical_var(nc, data_var)
        time_var = nu.find_time_var(nc, data_var)

        # Neither axis is present - throw an error
        if z_var is None and time_var is None:
            raise ValueError("Data is 3D but there is no vertical or time axis")

        if z_var is not None:
            # We have a z-axis
            return data_var[z_index,:,:]
        else:
            # We have a time axis
            return data_var[t_index,:,:]
    else:
        # num_dims must equal 4
        return data_var[t_index,z_index,:,:]


def extract_vertical_data(nc, data_var, direction, value, t_index):
    """
    This function extracts data ready to be plotted on the vertical cross section.
    :param nc: a NetCDF Dataset object
    :param data_var: a NetCDF Variable object representing the variable to be extracted
    :param direction: the direction of the vertical section as a string
    :param value: the latitude or longitude that section represents
    :return: the extracted vertical profile data and coordinate data for plotting
    """
    # Find the number of dimensions for the data variable
    num_dims = len(data_var.dimensions)
    if num_dims < 3 or num_dims > 4:
        raise ValueError("Cannot extract data from variable with %d dimensions" % num_dims)
    lon_var = nu.find_longitude_var(nc, data_var)
    lat_var = nu.find_latitude_var(nc, data_var)
    t_var = nu.find_time_var(nc, data_var)
    z_var = nu.find_vertical_var(nc, data_var)

    if lon_var is None or lat_var is None:
        # Vertical cross section need both latitude and longitude
        raise ValueError("Cannot plot vertical cross section without both \
                         longitude and latitude")
    else:
        # Determine the direction of this section and find the index of the coordinate value
        if (direction == 'NS'):
            sec_index = nu.find_nearest_lon_index(nc, data_var, value)
            # Check the existing of vertical dimension
            if z_var is None:
                raise ValueError("Cannont plot vertical cross section without vertical dimension")               
            elif t_var is None:
                # Return 3-D array, x- and z- coordinate data if time dimension does not exist
                return data_var[:,:,sec_index], lat_var, z_var
            else:
                # Return 4-D array, x- and z- coordinate data if time dimension exists
                return data_var[t_index,:,:,sec_index], lat_var, z_var
                    
        elif (direction == 'EW'):
            sec_index = nu.find_nearest_lat_index(nc, data_var, value)
            if z_var is None:
                raise ValueError("Cannont plot vertical cross section without vertical dimension")               
            elif t_var is None:
                return data_var[:,sec_index,:], lon_var, z_var
            else:
                return data_var[t_index,:,sec_index,:], lon_var, z_var
                
        else:
            raise ValueError("Need to choose the direction from NS or EW") 
    
    
def extract_timeseries(nc, data_var, lon, lat, z):
    """
    This function extracts data ready to be plotted the time series.
    :param nc: a NetCDF Dataset object
    :param data_var: a NetCDF Variable object representing the variable to be extracted
    :param lon: the value of longitude in degrees
    :param lat: the value of latitude in degrees
    :param z: the value of vertical coordinate variable
    :return: the extracted data and coordinate data for plotting
    """
    # Find the number of dimensions for the data variable
    num_dims = len(data_var.dimensions)
    # To plot time series the data should have x-, y- and t- dimensions at least
    if num_dims < 3 or num_dims > 4:
        raise ValueError("Cannot extract data from variable with %d dimensions" % num_dims)
    lon_var = nu.find_longitude_var(nc, data_var)
    lat_var = nu.find_latitude_var(nc, data_var)
    t_var = nu.find_time_var(nc, data_var)
    z_var = nu.find_vertical_var(nc, data_var)
    
    if t_var is None:
        # Time series plot must contain the time dimension
        raise ValueError("The data does not have time dimension")
    # Consider other dimensions when time diemension exists
    elif lon_var is None or lat_var is None:
        # Time series plot needs both latitude and longitude to determine location
        raise ValueError("Cannot plot time series plot without both longitude \
                         and latitude")
    # Check the existence of vertical axis variable
    elif z_var is not None:
        lon_index = nu.find_nearest_lon_index(nc, data_var, lon)
        lat_index = nu.find_nearest_lat_index(nc, data_var, lat)
        z_index = nu.find_nearest_z_index_index(nc, data_var, z)
        return data_var[:,z_index,lat_index,lon_index], t_var
    else:
        lon_index = nu.find_nearest_lon_index(nc, data_var, lon)
        lat_index = nu.find_nearest_lat_index(nc, data_var, lat)
        return data_var[:,lat_index,lon_index], t_var
    
    
