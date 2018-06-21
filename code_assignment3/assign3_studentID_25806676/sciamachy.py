import numpy as np
import matplotlib.pyplot as plt

def plot_sciamachy(filename):
    """
    This function reads the SCIAMACHY data file and plots the file as a 
    scatter plot.
    :param filename: the name of the SCIAMACHY file
    :return: no return
    """
    # Reading the data from the csv files
    r = np.recfromcsv(filename)
    
    # Plotting the scatter plot
    plt.figure()
    plt.scatter(r.lon, r.lat, c = r.o3_du,  edgecolors='none')
    plt.colorbar()
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.title('The measurement of ozone by satellite ENVISAT on 20th August 2006')
    plt.show()
    
