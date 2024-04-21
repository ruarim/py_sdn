# librays deps
from random import randrange

# classes and utilites
from point_3D import Point3D
from room import Room
from scattering_junction import ScatteringJunction
from propigation_line import PropigationLine
from source import Source
from mic import Mic

def rand_point(min, max):
    return Point3D(randrange(min, max), 
                   randrange(min, max), 
                   randrange(min, max),)
  
# setup the simulation
room_dims = [5, 5, 5]
# source_location = Point3D(0.3, 0.5, 0.9)
# mic_location = Point3D(0.4, 0.1, 0.4)
# room = Room(room_dims[0], room_dims[1], room_dims[2], source_location, mic_location)
# create a room
    # shape, x, y, z
    # source = Point3D(x,y,z)
    # mic    = Point3D(x,y,z)
# for each wall find reflection location

# for each reflection create scattering junction

# create source
source_location = Point3D(0.3, 0.5, 0.9)
source = Source(source_location)

# create mic
mic_location = Point3D(0.3, 0.5, 0.9)
mic = Mic(mic_location)

# create direct path
direct_path = PropigationLine(start=source, end=mic)
source.add_direct_path(direct_path)
mic.add_direct_path(direct_path)

# for each scattering junction create N input and output propigation lines
# where M = number of scattering nodes
# each junction has M output prop lines
# which are inputs for all other junction
M = 3 # reflections 
junctions: list[ScatteringJunction] = []

# for each refelection create a scattering junction
for i in range(M):
    junction_loc = rand_point(0, room_dims[0]) # should come from reflections
    junction = ScatteringJunction(junction_loc, source, mic)
    junctions.append(junction)

print(junctions)

for i in range(M):    
    # connect source to junction
    source_line = PropigationLine(start=source, end=junctions[i])
    source.add_to_junction(source_line)
    # connect junction to mic
    mic_line = PropigationLine(start=junctions[i], end=mic)
    mic.add_from_junction(mic_line)
    
    # connect refelection to all other reflections via propigations lines
    for j in range(M):
        # ignore diagonal - dont connect node to itself
        if i == j: continue
        
        # create the connection: junction i --prop line--> junction j
        prop_line = PropigationLine(start=junctions[i], end=junctions[j])
        
        # append in/out line
        junctions[i].add_out(prop_line)
        junctions[j].add_in(prop_line)
        
# run the simulation 
# the source writes to propigation lines connected to all junctions and the microphone
# the junctions write to and read from all other junctions via bidirectional propigation lines (waveguides)
# the junctions write to propigation lines connected to the mic
# the mic reads from propigation lines connected to the junction
# and the mic reads from the direct path propigation line

