""" Useful helper methods and utility functions """
import numpy as np

def find_nearest_index(vals, target):
    """
    Searches through vals for the target value, returning the index
    of the value in vals that is closest numerically to the target value.
    If more than one value in vals is equally close to the target, the index
    of the first value will be returned.
    :param vals: an array/list of values
    :param target: a value for which to search the array
    :return: index in vals of value nearest to target
    """
    # np.argmin() returns the indices of minimum value along an axis.
    # so subtract value from all entries in value_array, take absolute result and
    # find index of minimum
    return (np.abs(np.array(vals) - float(target))).argmin()
    
# Test functions for find_nearest_index
# Simply run this script to run the tests
# Note that these tests are very basic.  A full set of tests would be much
# longer and more comprehensive!
if __name__ == '__main__':
    # create a set of values from 0 to 99 inclusive
    arr = range(0,100)
    ni = find_nearest_index(arr, -0.1)
    print "ni = %s, should be 0" % ni
    ni = find_nearest_index(arr, 0.1)
    print "ni = %s, should be 0" % ni
    ni = find_nearest_index(arr, 23.1)
    print "ni = %s, should be 23" % ni
    ni = find_nearest_index(arr, 23.8)
    print "ni = %s, should be 24" % ni
    ni = find_nearest_index(arr, 98.9)
    print "ni = %s, should be 99" % ni
    ni = find_nearest_index(arr, 100)
    print "ni = %s, should be 99" % ni
