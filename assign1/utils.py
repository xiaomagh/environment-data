"""
student ID : 25806676
"""

def square_all(num):
    """
    Create a function for calculating the square number list of input list 
    """
    for i in range(len(num)):
         num[i] = num[i]**2    
    return num

import numpy as np         
def root_mean_square(num):
    """
    Create a function for calculating the root mean square of input list
    """
    sum = 0.
    N = len(num)
    for i in range(N):
        sum = sum + num[i]**2        
    rms = np.sqrt(sum/N)
    return rms
    
def find_nearest_index(num,value):
    """
    Create a function which outputs the index of the number in input list that 
    is the nearest to the target value
    """
    N = len(num)
# Create new list which contains the differnces between target value and list
    diff = np.zeros(N) 
    for i in range(N):
        diff[i] = abs(value - num[i])
    for j in range(N):
        if diff[j] == np.min(diff): # Find the nearest index
            return j
    
    
    