# image method refelection calculation
# when given room dimensions, source and microphone
# find early reflections coords on each wall
from utils.point3 import Point3

# shoebox reflecftion points 
def find_reflections(room_dims, source_pos, receiver_pos):
    L, W, H = room_dims
    S_x, S_y, S_z = source_pos
    R_x, R_y, R_z = receiver_pos

    # Define image source positions
    image_sources = [
        (-S_x, S_y, S_z),        # Front wall
        (2 * L - S_x, S_y, S_z), # Back wall
        (S_x, -S_y, S_z),        # Left wall
        (S_x, 2 * W - S_y, S_z), # Right wall
        (S_x, S_y, -S_z),        # Floor
        (S_x, S_y, 2 * H - S_z)  # Ceiling
    ]

    def intersection_param(I, R, boundary_val, axis):
        if axis == 'x':
            return (boundary_val - I[0]) / (R[0] - I[0])
        elif axis == 'y':
            return (boundary_val - I[1]) / (R[1] - I[1])
        elif axis == 'z':
            return (boundary_val - I[2]) / (R[2] - I[2])

    intersections: list[Point3] = []

    boundaries = [
        (0, 'x'), (L, 'x'),  # x boundaries
        (0, 'y'), (W, 'y'),  # y boundaries
        (0, 'z'), (H, 'z')   # z boundaries
    ]

    for I in image_sources:
        for boundary_val, axis in boundaries:
            t = intersection_param(I, receiver_pos, boundary_val, axis)
            if 0 <= t <= 1:
                intersection_point = Point3(
                    I[0] + t * (R_x - I[0]),
                    I[1] + t * (R_y - I[1]),
                    I[2] + t * (R_z - I[2])
                )
                intersections.append(intersection_point)
    
    return intersections
