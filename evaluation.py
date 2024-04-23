# an evaluation of 
# - t60 againt sabine and eyring formulas
# - echo density
# - mode density

# direct path component should be removed for evaluation

import numpy as np

def calc_volume():
    pass

def calc_surface_areas():
    pass

def sabine_T60(V: float, A, alpha):
    """
    Calculate reverberation time using Sabine's formula.
    
    Parameters:
    V (float): Volume of the room in cubic meters.
    A (numpy array): Array of surface areas of materials in square meters.
    alpha (numpy array): Array of absorption coefficients of materials.
    
    Returns:
    float: Reverberation time in seconds.
    """
    if np.any(alpha < 0) or np.any(alpha > 1):
        raise ValueError("Absorption coefficients should be between 0 and 1.")
    return (0.161 * V) / np.sum(A * alpha)


import numpy as np

def eyring_T60(V: float, A, alpha):
    """
    Calculate reverberation time using Eyring's formula.
    
    Parameters:
    V (float): Volume of the room in cubic meters.
    A (numpy array): Array of surface areas of materials in square meters.
    alpha (numpy array): Array of absorption coefficients of materials (dimensionless).
    
    Returns:
    float: Reverberation time in seconds.
    """
    if np.any(alpha < 0) or np.any(alpha > 1):
        raise ValueError("Absorption coefficients should be between 0 and 1.")
    
    total_absorption = np.sum(A * alpha)
    total_area = np.sum(A)
    
    if total_absorption >= total_area:
        raise ValueError("Total absorption cannot be greater than or equal to total area.")
    
    return (0.161 * V) / (-total_area * np.log(1 - total_absorption / total_area)) # is "-total_area" correct
