# classes and utilites
from point_3D import Point3D
from scattering_junction import ScatteringJunction
from propigation_line import PropigationLine
from source import Source
from mic import Mic
from config import SIGNAL_LENGTH, FS, WALL_ABSORPTION, OUTPUT_TO_FILE, ROOM_DIMS, SOURCE_LOC, MIC_LOC, BURST_LENGTH, TEST_SIGNAL
from utils import write_array_to_wav, plot_signal, plot_in_vs_out
from reflections import find_reflections
from signals import test_signal, zeros

# create source
source_location = Point3D(SOURCE_LOC[0], SOURCE_LOC[1], SOURCE_LOC[2])
source = Source(source_location)

# create mic
mic_location = Point3D(MIC_LOC[0], MIC_LOC[1], MIC_LOC[2])
mic = Mic(mic_location)

# create direct path
direct_path = PropigationLine(start=source, end=mic)
direct_path.attenuation = min(1 / direct_path.distance, 1)
source.add_direct_path(direct_path)
mic.add_direct_path(direct_path)

# for each scattering junction create M bidirectional propigation lines
# where M = number of reflections 
# each junction has M output prop lines which are inputs for all other junction

# find early reflections in shoebox room
early_reflections = find_reflections(ROOM_DIMS, source.location)

M = len(early_reflections)
junctions: list[ScatteringJunction] = []

# for each refelection create a scattering junction
for i in range(M):
    junction_loc = early_reflections[i]
    junction = ScatteringJunction(junction_loc, source, mic, alpha=WALL_ABSORPTION)
    junctions.append(junction)

# connect the scattering junctions
for i in range(M):    
    # connect source to junction
    source_line = PropigationLine(start=source, end=junctions[i])
    source_attenuation = 1 / source_line.distance
    source_line.attenuation = min(source_attenuation, 1) # set the gain to 1 if > 1
    source.add_to_junction(source_line)
    
    # connect junction to mic
    mic_line = PropigationLine(start=junctions[i], end=mic)
    mic_attenuation = 1 / (1 + (mic_line.distance / source_line.distance))
    mic_line.attenuation = min(mic_attenuation, 1)
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
signal_in  = test_signal(TEST_SIGNAL, SIGNAL_LENGTH, BURST_LENGTH, FS)
signal_out = zeros(SIGNAL_LENGTH)

print("processing samples...")
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
        out, sample_to_mic = junctions[i].scatter_in(source_sample)
        junctions[i].scatter_out(out)
        # push scattered sample to microphone prop line
        mic.propigation_lines[i].sample_in(sample_to_mic)
        # sum signal from mic propigation lines - prefer a call to mic.process
        output += mic.propigation_lines[i].sample_out()
                
    # model the microphone here
    # output = mic.process() - remove summation of mic sample_out above
    
    # model mic orientation with left right gain
    
    # output the sample at current index
    signal_out[s] = output + direct_path.sample_out()

print("writing to file...")
file_name = f"IR_junctions:{M}_wall-attenuation:{WALL_ABSORPTION}_fs:{FS}_room:{ROOM_DIMS}_source:{SOURCE_LOC}_mic:{MIC_LOC}"
if(OUTPUT_TO_FILE): write_array_to_wav(file_name, signal_out, FS)

print("plotting...")
plot_signal(signal_in, title="Input signal")
plot_signal(signal_out, title=f"Room Dimensions: {ROOM_DIMS}, Source: {SOURCE_LOC}, Mic: {MIC_LOC}, wall absorption: {WALL_ABSORPTION}")
plot_in_vs_out(signal_in, signal_out)