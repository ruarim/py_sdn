# image method refelection calculation
# when given room dimensions, source and microphone
# find early reflections coords on each wall
from source import Source
from utils.vec3 import Vec3

# shoebox reflecftion points - for now this is over simplified
def find_reflections(room: list[int], source_loc: Vec3):
    reflections = [
        Vec3(source_loc.x, source_loc.y, room[2]), # ceiling - source x, y room.z
        Vec3(source_loc.x, source_loc.y, 0),       # floor - source x, y, 0
        Vec3(source_loc.x, room[1], source_loc.z), # right - source x, room.y source z
        Vec3(source_loc.x, 0, source_loc.z),       # left - source x, 0, source z
        Vec3(room[0], source_loc.y, source_loc.z), # back - room.x, source y z
        Vec3(0, source_loc.y, source_loc.z)        # front -  0, source y, z
    ]

    return reflections