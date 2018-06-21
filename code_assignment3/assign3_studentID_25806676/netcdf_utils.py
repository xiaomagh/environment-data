
from utils import *

""" This module contains code for reading data from NetCDF files and
    intepreting metadata """


def get_attribute(var, att_name, default=None):
    """
    Gets the value of the given attribute as a string.  Returns the
    given default if the attribute is not defined. This is a useful
    "helper" method, which avoids AttributeErrors being raised if the
    attribute isn't defined.  If no default is specified, this function
    returns None if the attribute is not found.
    :param var: NetCDF Variable object
    :param att_name: name of attribute
    :param default: optional - specify return if attribute is not found
    :return: value of attribute or default
    """
    if att_name in var.ncattrs():
        return var.getncattr(att_name)
    else:
        return default


def get_title(var):
    """
    Returns a title for a variable in the form "name (units)"
    The name is taken from the standard_name if it is provided, but
    if it is not provided, it is taken from the id of the variable
    (i.e. var._name).  If the units are not provided, the string
    "no units" is used instead.
    :param var: NetCDF Variable object
    :return: title for variable
    """

    # Obtain standard name, or use var._name if it's not found
    standard_name = get_attribute(var, 'standard_name', var._name)
    # Obtain units, or use 'no units' if not found
    units = get_attribute(var, 'units', 'no units')
    # Return string
    return " %s (%s) " % (standard_name, units)

#######################################################################################
#####  The following functions test to see if coordinate variables represent geographic
#####  or time axes
#######################################################################################


def is_longitude_var(coord_var):
    """
    Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable holds values of longitude, False otherwise
    :param coord_var: NetCDF Variable object
    :return: True if longitude, False otherwise
    """
    # In the Climate and Forecast conventions, longitude variables are indicated
    # by their units (not by their names)
    units = get_attribute(coord_var, 'units')
    # There are many possible options for valid longitude units
    if units in ['degrees_east', 'degree_east', 'degree_E', 'degrees_E', 'degreeE', 'degreesE']:
        return True
    else:
        return False


def is_latitude_var(coord_var):
    """
    Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable holds values of latitude, False otherwise
    :param coord_var: NetCDF Variable object
    :return: True if latitude, False otherwise
    """
    # In the Climate and Forecast conventions, latitude variables are indicated
    # by their units (not by their names)
    units = get_attribute(coord_var, 'units')
    # There are many possible options for valid latitude units
    if units in ['degrees_north', 'degree_north', 'degree_N', 'degrees_N', 'degreeN', 'degreesN']:
        return True
    else:
        return False


def is_vertical_var(coord_var):
    """
    Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable represents a vertical coordinate, False otherwise
    :param coord_var: NetCDF Variable object
    :return: True if vertical coordinate, False otherwise
    """
    # In the Climate and Forecast conventions, vertical coordinates are indicated
    # by units of pressure, or by the presence of a "positive" attribute.
    units = get_attribute(coord_var, "units")
    # First we look for units of pressure.  (There may be more possible pressure units
    # than are used here.)
    if units in ['Pa', 'hPa', 'pascal', 'Pascal']:
        return True
    else:
        # We don't have units of pressure, but perhaps we have a "positive" attribute
        positive = get_attribute(coord_var, 'positive')
        if positive in ['up', 'down']:
            return True
            
    # If we've got this far, we haven't satisfied either of the conditions for a
    # valid vertical axis
    return False


def is_time_var(coord_var):
    """
    Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable represents a time coordinate, False otherwise
    :param coord_var: NetCDF Variable object
    :return: True if time coordinate, False otherwise
    """
    # In the Climate and Forecast conventions, time coordinates are indicated
    # by units that conform to the pattern "X since Y", e.g. "days since 1970-1-1 0:0:0".
    # For simplicity, we just look for the word "since" in the units.  A complete
    # implementation should check this more thoroughly.
    units = get_attribute(coord_var, 'units')
    if units is None:
        # There are no units, so this can't be a time coordinate variable
        return False
    # The "find()" function on strings returns the index of the first match of the given
    # pattern.  If no match is found, find() returns -1.
    if units.find("since") >= 0:
        return True
    else:
        return False


#######################################################################################
#####  The following functions find geographic and time coordinate axes
#####  for data variables.
#######################################################################################

# As you can see, there is a lot of repetition in these functions - they all do basically
# the same thing.  There is a way to avoid this repetition, but it involves a technique
# that you may not be familiar with (i.e. passing functions as arguments to other functions)
# - see me if you want to know more.
    
def find_longitude_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    longitude axis for the data variable.  If no longitude axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: longitude axis variable object or None
    """
    # First we iterate over the dimensions of the data variable
    for dim in data_var.dimensions:
        # We get the coordinate variable that holds the values for this dimension
        coord_var = nc.variables[dim]
        # We test to see if this is a longitude variable, if so we return it
        if is_longitude_var(coord_var):
            return coord_var
    # If we get this far we have not found the required coordinate variable
    return None


def find_latitude_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    latitude axis for the data variable.  If no latitude axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: latitude axis variable object or None
    """
    # Iterate over dimensions
    for dim in data_var.dimensions:
        # Get co-ord var holding values for this dimension
        coord_var = nc.variables[dim]
        # Is it a latitude variable?
        if is_latitude_var(coord_var):
            return coord_var
    # Not found
    return None


def find_vertical_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    vertical axis for the data variable.  If no vertical axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: vertical axis variable object or None
    """
    # Iterate over dimensions
    for dim in data_var.dimensions:
        # Get co-ord var holding values for this dimension
        coord_var = nc.variables[dim]
        # Is it a vertical variable?
        if is_vertical_var(coord_var):
            return coord_var
    # Not found
    return None


def find_time_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    time axis for the data variable.  If no time axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: time axis variable object or None
    """
    # Iterate over dimensions
    for dim in data_var.dimensions:
        # Get co-ord var holding values for this dimension
        coord_var = nc.variables[dim]
        # Is it a time variable?
        if is_time_var(coord_var):
            return coord_var
    # Not found
    return None


def isPositiveUp(z_var):
    """
    Given a vertical coordinate variable, this function returns true if the
    values on the vertical axis increase upwards. For vertical axes based on pressure,
    the values increase downward, so this returns False.  If the axis is not based
    on pressure, the value of the "positive" attribute (which can be "up" or "down")
    is used instead. Will not work if anything other than a valid variable object is input.
    :param z_var: vertical coordinate NetCDF Variable object
    :raise ValueError: if it's not a valid vertical coordinate variable
    :return: True if values increase upwards, False otherwise
    """
    # First check for valid units of pressure
    units = get_attribute(z_var, 'units')  # Gives None if no units
    if units in ['Pa', 'hPa', 'pascal', 'Pascal', 'bar', 'millibar', 'decibar', 'atmosphere', 'atm', 'mb']:
        return False  # Pressure increases downward

    # Then check for positive attribute
    direction = get_attribute(z_var, 'positive')
    if direction == None:
        raise ValueError(
            "Not a valid height or depth (ie vertical) axis; CF conventions dictate a vertical axis must "
            "have either valid units of pressure or the positive attribute set to 'up' or 'down'")
    else:
        if direction.lower() == "up":
            return True
        elif direction.lower() == "down":
            return False
        else:
            # Raise value error
            raise ValueError(
                "%s is not a valid value for the positive attribute; CF conventions state it must be set "
                "to 'up' or 'down'" % direction)
                
                
def find_nearest_lat_index(nc, data_var, target):
    """
    Given a NetCDF Dataset object, one variable object which can represent the data variable,
    and a provided latitude value, to find the coordinate variable representing the 
    latitude of the data variable which is the closest to the provided latitude and
    return the index of the found latitude    
    :param nc: the NetCDF Dataset object
    :param data_var: the NetCDF Variable object
    :param target: the provided latitude value
    :raise ValueError: if there's no corresponding latitude coordinate variable
    :return: the index of the latitude variable closest to the provided value
    """
    # Find the latitude coordinate variable of the data variable
    lat = find_latitude_var(nc, data_var)
    # Check whether latitude variable exists
    if (lat == None):
        # Raise ValueError
        raise ValueError("There is no latitude coordinate variable found")
    else:
        # Find the nearest latitude index
        index_lat = find_nearest_index(lat, target)
        
        return index_lat
        
        
def find_nearest_z_index(nc, data_var, target):
    """
    Given a NetCDF Dataset object, one variable object which can represent the data variable,
    and a provided vertical axis value, to find the coordinate variable representing the 
    vertical axis of the data variable which is the nearest to the provided one, and
    return the index of the found vertical axis value    
    :param nc: the NetCDF Dataset object
    :param data_var: the NetCDF Variable object
    :param target: the provided vertical axis value
    :raise ValueError: if there's no corresponding vertical coordinate variable
    :return: the index of the vartical coordinate variable closest to the provided target
    """
    # Find the vertical coordinate variable of the data variable
    vert = find_vertical_var(nc, data_var)
    # Check whether vertical axis variable exists
    if (vert == None):
        # Raise ValueError
        raise ValueError("There is no vertical coordinate variable found")
    else:
        # Find the nearest vertical axis value index
        index_vert = find_nearest_index(vert, target)
        
        return index_vert
  
  
def find_nearest_lon_index(nc, data_var, target):
    """
    Given a NetCDF Dataset object, one variable object which can represent the data variable,
    and a provided longitude variable value, to find the coordinate variable representing the 
    longitude of the data variable which is the nearest to the provided one, and
    return the index of the found longitude variable value    
    :param nc: the NetCDF Dataset object
    :param data_var: the NetCDF Variable object
    :param target: the provided longitude value
    :raise ValueError: if there's no corresponding longitude coordinate variable
    :return: the index of the longitude coordinate variable closest to the provided target
    """
    # Find the vertical coordinate variable of the data variable
    lon = find_longitude_var(nc, data_var)
    # Check whether vertical axis variable exists
    if (lon == None):
        # Raise ValueError
        raise ValueError("There is no longitude coordinate variable found")
    else:
        # Find the nearest longitude coordinate value index
        
        # Convert the angles value into radians value
        diff = (np.array(lon)-target)/180.*np.pi
        index_lon = find_nearest_index(np.cos(diff), 1.0)
    
        return index_lon