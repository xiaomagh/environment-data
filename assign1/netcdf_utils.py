# -*- coding: utf-8 -*-
"""
student number: 25806676
"""
import numpy as np
import netCDF4

def is_longitude_var(obj):
    """
    This function aims to test whether the variable represents a valid 
    longitude variable
    """
    if (obj.name =='longitude'):
        return True
    else:
        return False


def find_longitude_var(nc,name):
    """
    This function aims to find the corresponding variable object using 
    the input name and then in all the dimension variables of this 
    variable, find whether the longitude variable exists
    """
    var_obj = nc.variables[name] # Find the corresponding variable object 
    dimens = var_obj.dimensions # Find the names of the dimensions of variable
    for i in range(len(dimens)):
        # For each dimension find the corresponding variable
        var_dim = nc.variables[dimens[i]]
        if is_longitude_var(var_dim) == True:
            return var_obj # If longitude exists, return the variable object
        
        return None
            
            
    
    
    