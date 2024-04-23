# image method refelection calculation
# when given room dimensions, source and microphone
# find early reflections coords on each wall
from source import Source
from point_3D import Point3D

# shoebox reflecftion points
def find_reflections(room: list[int], source_loc: Point3D):
    reflections = [
        Point3D(source_loc.x, source_loc.y, room[2]), # ceiling - source x, y room.z
        Point3D(source_loc.x, source_loc.y, 0),       # floor - source x, y, 0
        Point3D(source_loc.x, room[1], source_loc.z), # right - source x, room.y source z
        Point3D(source_loc.x, 0, source_loc.z),       # left - source x, 0, source z
        Point3D(room[0], source_loc.y, source_loc.z), # back - room.x, source y z
        Point3D(0, source_loc.y, source_loc.z)        # front -  0, source y, z
    ]

    return reflections