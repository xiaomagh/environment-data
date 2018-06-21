# This is a sample test program for assignment1
import utils
from netCDF4 import Dataset
import netcdf_utils


def check_lists_equal(list_1, list_2):
    """
    Checks if two sequences contain same elements.  Useful for
    checking if a list is equal to a numpy array.
    """
    if list_1 is None:
        if list_2 is None:
            return True
        else:
            return False
    elif list_2 is None:
        # We know that list_1 is not None
        return False
    if len(list_1) != len(list_2):
        return False
    for i in range(len(list_1)):
        if list_1[i] != list_2[i]:
            return False
    return True


def check_floats_equal(flt_1, flt_2, tol=1e-6):
    """
    Checks if two numbers are equal within tolerance
    """
    if abs(flt_1 - flt_2) < tol:
        return True
    else:
        return False


def main():
    """
    Simple test harness for assignment1 functions - incomplete.
    """
    print 'Squaring [1,2,3,4,5]:', utils.square_all([1, 2, 3, 4, 5])

    print 'Finding RMS of [1,2,3,4,5]:', utils.root_mean_square([1, 2, 3, 4, 5])

    print 'Finding index of number closest to zero in [1,2,3,4,5]:', utils.find_nearest_index([1, 2, 3, 4, 5], 0)

    # Set up dummy dataset / variable to test method names
    ds = Dataset('/test3.nc', 'w')
    lat_dim = ds.createDimension('latitude', 180)
    v = ds.createVariable('latitude', 'f8', ('latitude',))
    v.units = 'degrees_north'
    ds.createVariable('temperature', 'f8', ('latitude',))

    print 'Checking if Variable is longitude:', netcdf_utils.is_longitude_var(v)

    print 'Finding if "temperature" has a longitude dimension in dataset:',\
        netcdf_utils.find_longitude_var(ds, 'temperature')

if __name__ == "__main__":
    main()
