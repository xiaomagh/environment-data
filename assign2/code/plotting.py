""" Contains code for displaying data """

import matplotlib.pyplot as plt

# Question 2.2: complete this!
# student number: 25806676
def display_map_plot(data, lons, lats, title):
    """
    Do not need to use the outer data in this function just plot the 
    2-D data by the input one with 20 kinds of contour colors
    """
    
    plt.figure()
    plt.contourf(lons, lats, data, 20)
    plt.colorbar()
    plt.xlabel('$longitute(degrees)$')
    plt.ylabel('$latitude(degrees)$')
    plt.title(title)
    plt.show()

