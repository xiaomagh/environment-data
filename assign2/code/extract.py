""" Contains code for extracting data from NetCDF files """

import netcdf_utils

# Question 2.1: Complete this!
# student number: 25806676
def extract_map_data(nc, data_var, t_index, z_index):
    """ TODO: add a docstring! """
    # Find the number of dimensions for the data variable
    num_dims = len(data_var.dimensions)
    if num_dims < 2 or num_dims > 4:
        # This shows an example of raising an exception if bad input means that we can't proceed further
        raise ValueError("Cannot extract data from variable with %d dimensions" % num_dims)
    # ... Complete this function!
    # Consider the abnormal situation that the longitude and latitude cannot 
    # be found in the nc variable
    if netcdf_utils.find_latitude_var == False or netcdf_utils.find_longitude_var == False:
        raise ValueError("the variable does not have latitude and longitude variables")
    # First check the existance of time dimension 
    if not netcdf_utils.find_time_var(nc, data_var):
        # Then check the existance of vertical dimension if cannot find the 
        # timen dimension
        if not netcdf_utils.find_vertical_var(nc, data_var):
            # If both of time and vertical dimension do not exist
            # only return 2-D array
            return data_var[:,:]
        else:
            # If only the time dimension does not exist then return the 3-D
            # array with z_index
            return data_var[z_index,:,:]
    else:
        # If time dimension exists, check the existance of vertical dimension
        if not netcdf_utils.find_vertical_var(nc, data_var):
            # if vertical dimension does not exist, return the 3-D array
            # with time dimension
            return data_var[t_index,:,:]
        else:
            # If both time and vertical dimension exist, ruturn the 4-D array
            return data_var[t_index,z_index,:,:]
        
        