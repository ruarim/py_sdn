# config values
from config import (
    SIGNAL_LENGTH, FS, WALL_ABSORPTION, OUTPUT_TO_FILE, 
    ROOM_DIMS, SOURCE_LOC, MIC_LOC, BURST_LENGTH, 
    TEST_SIGNAL, PLOT, CHANNEL_LEVELS, DATA_DIR, FILE_NAME
)

# classes and utilites
from point_3D import Point3D
from network import Network
from utils import write_array_to_wav, plot_signal, plot_in_vs_out
from reflections import find_reflections
from signals import test_signal, zeros, signal_duplicator

# setup the delay network
source_location = Point3D(SOURCE_LOC[0], SOURCE_LOC[1], SOURCE_LOC[2])
mic_location = Point3D(MIC_LOC[0], MIC_LOC[1], MIC_LOC[2])
early_reflections = find_reflections(ROOM_DIMS, source_location)
sdn = Network(early_reflections, source_location, mic_location, WALL_ABSORPTION, FS) 

# input / output arrays
signal_in  = test_signal(TEST_SIGNAL, SIGNAL_LENGTH, FS, BURST_LENGTH, data_dir=DATA_DIR, file_name=FILE_NAME)
signal_out = zeros(SIGNAL_LENGTH)
channels   = len(CHANNEL_LEVELS)
stereo_out = signal_duplicator(signal_out)
# stereo_in = signal_duplicator(signal_in)

# run the simulation
print("processing samples...")
for s in range(len(signal_in)):
    # process the current sample  
    sample = signal_in[s]
    signal_out[s] = sdn.process(sample)
    
    # to model stereo source and mic should extra nodes be added
    # or should the simulation be run for both channels with modeling of directivity via gain at output
    for c in range(channels):
        # model mic orientation with left right gain
        level = CHANNEL_LEVELS[c]
        stereo_out[s][c] = signal_out[s] * level

# output and plot the results
if(OUTPUT_TO_FILE): 
    print("writing to file...")
    file_name = f"IR_junctions:{len(early_reflections)}_wall-attenuation:{WALL_ABSORPTION}_fs:{FS}_room:{ROOM_DIMS}_source:{SOURCE_LOC}_mic:{MIC_LOC}"
    write_array_to_wav(file_name, stereo_out, FS)

if(PLOT):
    print("plotting...")
    plot_signal(signal_in, title="Input signal")
    plot_signal(signal_out, title=f"Room Dimensions: {ROOM_DIMS}, Source: {SOURCE_LOC}, Mic: {MIC_LOC}, wall absorption: {WALL_ABSORPTION}")
    plot_in_vs_out(signal_in, signal_out)