import numpy as np
from utils.point3 import Point3

def find_reflections(room_dims: list[float], source: list[float], receiver: list[float], order: int):
    L, W, H = room_dims
    S_x, S_y, S_z = source
    R_x, R_y, R_z = receiver

    # Initialize the list of image sources with the original source
    image_sources = [(S_x, S_y, S_z)]
    
    # Boundaries
    boundaries = [
        (0, 'x'), (L, 'x'),  # x boundaries
        (0, 'y'), (W, 'y'),  # y boundaries
        (0, 'z'), (H, 'z')   # z boundaries
    ]

    # Function to reflect a point across a boundary
    def reflect_point(point, boundary_val, axis):
        if axis == 'x':
            return (2 * boundary_val - point[0], point[1], point[2])
        elif axis == 'y':
            return (point[0], 2 * boundary_val - point[1], point[2])
        elif axis == 'z':
            return (point[0], point[1], 2 * boundary_val - point[2])
    
    # Generate image sources for each order
    for _ in range(order):
        new_sources = []
        for I in image_sources:
            for boundary_val, axis in boundaries:
                reflected_point = reflect_point(I, boundary_val, axis)
                new_sources.append(reflected_point)
        image_sources.extend(new_sources)

    # Remove duplicate image sources
    image_sources = list(set(image_sources))
    
    def intersection_param(I, R, boundary_val, axis):
        if axis == 'x':
            denominator = R[0] - I[0]
        elif axis == 'y':
            denominator = R[1] - I[1]
        elif axis == 'z':
            denominator = R[2] - I[2]

        # If source and receiver have the same value along this axis, skip this axis
        if np.isclose(denominator, 0):
            return None
        
        return (boundary_val - I[0 if axis == 'x' else (1 if axis == 'y' else 2)]) / denominator

    intersections = set()

    # Calculate intersection points
    for I in image_sources:
        for boundary_val, axis in boundaries:
            t = intersection_param(I, receiver, boundary_val, axis)
            if t is not None and 0 <= t <= 1:
                intersection_point = Point3(
                    I[0] + t * (R_x - I[0]),
                    I[1] + t * (R_y - I[1]),
                    I[2] + t * (R_z - I[2])
                )
                # Filter out reflections outside the room boundaries
                if 0 <= intersection_point.x <= L and 0 <= intersection_point.y <= W and 0 <= intersection_point.z <= H:
                    intersections.add(intersection_point)
                    print(intersection_point.to_list())
    
    return list(intersections)
