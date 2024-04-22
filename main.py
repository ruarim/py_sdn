# librays deps
from random import randrange
import numpy as np
from matplotlib import pyplot as plt

# classes and utilites
from point_3D import Point3D
from room import Room
from scattering_junction import ScatteringJunction
from propigation_line import PropigationLine
from source import Source
from mic import Mic
from constants import SIGNAL_LENGTH, FS
from utils import write_array_to_wav

# temp utility function for creating random reflections
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
mic_location = Point3D(0.4, 0.1, 0.4)
mic = Mic(mic_location)

# create direct path
direct_path = PropigationLine(start=source, end=mic)
source.add_direct_path(direct_path)
mic.add_direct_path(direct_path)

# for each scattering junction create M bidirectional propigation lines
# where M = number of scattering nodes
# each junction has M output prop lines
# which are inputs for all other junction
M = 6 # reflections 
junctions: list[ScatteringJunction] = []
wall_attenuation = 0.9

# for each refelection create a scattering junction
for i in range(M):
    junction_loc = rand_point(0, room_dims[0])
    junction = ScatteringJunction(junction_loc, source, mic, wall_attenuation=wall_attenuation)
    junctions.append(junction)

# connect the scattering junctions
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
        # create the connection: junction i --propigation line--> junction j
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

# input / output arrays
signal_in  = np.zeros(SIGNAL_LENGTH, dtype=np.float32)
signal_out = np.zeros(SIGNAL_LENGTH, dtype=np.float32)
# create unit impulse
signal_in[0] = 1.0

# process the input signal
for s in range(len(signal_in)):
    sample = signal_in[s]
    # add sample to direct path
    direct_path.sample_in(sample)
    
    output = 0.0
    for i in range(M):
        # push sample to source prop line
        source.propigation_lines[i].sample_in(sample) 
        # get sample from source propline
        source_sample = source.propigation_lines[i].sample_out()
        # apply scattering
        out, sample_to_mic = junctions[i].scatter_out(source_sample)

        junctions[i].scatter_in(out)
                
        # push scattered sample to microphone prop line
        mic.propigation_lines[i].sample_in(sample_to_mic)
        # sum signal from mic propigation lines
        output += mic.propigation_lines[i].sample_out()
                
    # output the sample at current index
    signal_out[s] = output + direct_path.sample_out()

# add other parameters to file name - source, mic, room dims etc
file_name = f"IR_junctions:{M}_wall-attenuation:{wall_attenuation}"
write_array_to_wav(file_name, signal_out, FS)

# plot impulse response
plt.figure(figsize=(10, 4))
plt.plot(signal_out)
plt.show()
