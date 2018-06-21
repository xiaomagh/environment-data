import netCDF4
import extract
import plotting
import netcdf_utils
# Windows OS paths can cause problems, you may need to use the 'os' module to help
import os

# Question 2.3: complete this!
# student number: 25806676
def plot_map(data_path, var, t_index, z_index):
    # Read the netcdf file
    nc = netCDF4.Dataset(data_path)
    # Read the particular variable by the input parameter
    data_var = nc.variables[var]
    # Extract the 2-D data of this var using the extract function
    data = extract.extract_map_data(nc, data_var, t_index, z_index)
    # find the longitude array
    lons = netcdf_utils.find_longitude_var(nc, data_var)
    lons = lons[:]
    # find the latitude array
    lats = netcdf_utils.find_latitude_var(nc, data_var)
    lats = lats[:]
    # Find the title by the get_title function created before
    title = netcdf_utils.get_title(data_var)
    # Plot the figure by map_plot function
    plotting.display_map_plot(data, lons, lats, title)

# Here are some test functions.
# Simply run this script to call them.
# (I will be using more tests than this, so be sure to test your code
# against lots of input files)

if __name__ == '__main__':
    # if you are using Windows and having problems with 'File Not Found',
    # you may need to convert the paths before accessing the files.
    # this one is on my PC, substitute your own as appropriate
    data_path = os.path.normpath(
        "C:/Users/xw904346/Documents/05_ReSC/09_SoftwareEngineering in Met/"
        "05_MTMD01_EnvVis/01_course_material/classes/lecture_03/data/polcoms.nc")
    plot_map(data_path, "POT", 0, 0)

    # so EITHER, convert the path...
    data_path = os.path.normpath("<your_path>/globmodel_temp.nc")
    plot_map(data_path, "ta", 0, 5)

    # ... OR you may be OK to put the file locations in directly
    plot_map("<your_path>/had_cem.nc", "salinity", 0, 5)

    plot_map("<your_path>/foam_natl.nc", "ssh", 0, 0)

    # The OSTIA dataset is large, so this test can be slow.  Uncomment
    # this line to run it
    plot_map("<your_path>/ostia.nc", "analysed_sst", 0, 5)

