# config values
from config import (
    SIGNAL_LENGTH, FS, WALL_ABSORPTION, OUTPUT_TO_FILE, 
    ROOM_DIMS, SOURCE_LOC, MIC_LOC, BURST_LENGTH, 
    TEST_SIGNAL, PLOT, CHANNEL_LEVELS, DATA_DIR, FILE_NAME,
    TIMER
)

# classes and utilites
from point_3D import Point3D
from network import Network
from room import Room
from utils import write_array_to_wav
from signals import test_signal, zeros, stack
from plot import plot_signal, plot_in_vs_out, plot_frequnecy_response, plot_T60
from evaluation import T60_evaluation
from performance import Performance

# start total runtime and setup timers
total_performance = Performance()
setup_performance = Performance()

# setup the delay network
source_location = Point3D(SOURCE_LOC[0], SOURCE_LOC[1], SOURCE_LOC[2])
mic_location = Point3D(MIC_LOC[0], MIC_LOC[1], MIC_LOC[2])
room = Room(ROOM_DIMS, source_location, mic_location) 
sdn = Network(room.early_reflections, source_location, mic_location, WALL_ABSORPTION, FS) 
setup_time = setup_performance.get_time()

# input / output arrays
channels = len(CHANNEL_LEVELS)
signal_in = test_signal(
    TEST_SIGNAL, 
    SIGNAL_LENGTH, 
    FS, 
    BURST_LENGTH, 
    data_dir=DATA_DIR, 
    file_name=FILE_NAME, 
    channels=channels
)
signal_out = stack(zeros(SIGNAL_LENGTH), channels)

# run the simulation
print("processing samples...")
# instead add multiple sources and mics to model multichannel
simulation_performance = Performance()
for c in range(channels):
    for s in range(len(signal_in)):
        # process the current sample
        sample = signal_in[s][c]
        sample_out = sdn.process(sample)  
        # model mic orientation with left right gain - use microphone array instead
        level = CHANNEL_LEVELS[c]
        signal_out[s][c] = sample_out * level

simulation_time = simulation_performance.get_time()
total_runtime = total_performance.get_time()
is_real_time, is_real_time_speedup = simulation_performance.is_real_time()

# show total run time
if TIMER:
    print(f"RUN TIME: {total_runtime}")
    print(f"SETUP TIME: {setup_time}")
    print(f"SIMULATION TIME: {simulation_time}")
    print(f"IS REAL TIME: {is_real_time}")
    print(f"IS REAL TIME WITH 10x SPEEDUP: {is_real_time_speedup}")
    
# output the result
if OUTPUT_TO_FILE: 
    print("writing to file...")
    file_name = f"IR_junctions:{len(sdn.junctions)}_wall-attenuation:{WALL_ABSORPTION}_fs:{FS}_room:{ROOM_DIMS}_source:{SOURCE_LOC}_mic:{MIC_LOC}"
    write_array_to_wav(file_name, signal_out, FS)

# plot the result
if PLOT:
    print("plotting...")
    # get mono signal for evaluation       
    mono_in = [s[0] for s in signal_in]
    mono_out = [s[0] for s in signal_out]
    # get sabine / eyring T60 values
    sabine, eyring = T60_evaluation(ROOM_DIMS, WALL_ABSORPTION)
    config_params = f"Room Dimensions: {ROOM_DIMS}, Source: {SOURCE_LOC}, Mic: {MIC_LOC}, wall absorption: {WALL_ABSORPTION}"
    # plot_signal(mono_in, title="Input signal")
    # plot_signal(mono_out, title=config_params)
    plot_in_vs_out(mono_in, mono_out)
    plot_T60(mono_out, sabine, eyring, FS, title="T60 - " + config_params)
    plot_frequnecy_response(mono_out, title=config_params)