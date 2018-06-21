""" This module contains code for reading data from NetCDF files and
    interpreting metadata """
    
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
    # Question 1.1: make this function work properly
    # student number: 25806676
    # Check whether there are units in the nc variables
    if get_attribute(var, 'units'): 
        units = get_attribute(var, 'units')
    else:
        units = "no units"
    # Check whether there are standard name in the nc variables     
    if get_attribute(var, 'standard_name'):
        return "%s(%s)"%(get_attribute(var, 'standard_name'),units)
    else:
        return "%s(%s)"%(var._name,units)
    
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
# the same thing.  There is a way to avoid this repetition, but it involves a rather
# advanced technique (i.e. passing functions as arguments to other functions).
# See me if you want to know more.
    
def find_longitude_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    longitude axis for the data variable.  If no longitude axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: longitude axis variable object
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
    :return: latitude axis variable object
    """
    for dim in data_var.dimensions:
        coord_var = nc.variables[dim]
        if is_latitude_var(coord_var):
            return coord_var
    return None

def find_vertical_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    vertical axis for the data variable.  If no vertical axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: vertical axis variable object
    """
    for dim in data_var.dimensions:
        coord_var = nc.variables[dim]
        if is_vertical_var(coord_var):
            return coord_var
    return None

def find_time_var(nc, data_var):
    """
    Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    time axis for the data variable.  If no time axis is found, this returns
    None.
    :param nc: NetCDF Dataset object
    :param data_var: NetCDF Variable object
    :return: time axis variable object
    """
    for dim in data_var.dimensions:
        coord_var = nc.variables[dim]
        if is_time_var(coord_var):
            return coord_var
    return None

def is_positive_up(z_var):
    """ Document how this function behaves """
    
    # Question 1.4: make this function work properly
    # student number: 25806676
    positive = get_attribute(z_var, 'positive')
    # Because the positive attribute has the value 'up' or 'down' and they are 
    # case insensitive, so we should consider about them as more as possible
    # if the positive values are not in the 'up' stock, we can think that the 
    # positive might be 'down', just return False directly
    if positive in ['up','UP','Up','uP','upward','UPWARD']:
        return True
    return False

