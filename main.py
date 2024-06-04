# librarys
from matplotlib import pyplot as plt
import numpy as np

# config values
from config import (
    SIGNAL_LENGTH, FS, WALL_ABSORPTION, OUTPUT_TO_FILE, 
    ROOM_DIMS, SOURCE_LOC, MIC_LOC, BURST_LENGTH, 
    TEST_SIGNAL, PLOT, CHANNEL_LEVELS, DATA_DIR, FILE_NAME,
    TIMER, DIRECT_PATH, ER_ORDER
)

# classes and utilites
from utils.point3 import Point3
from network import Network
from room import Room
from utils.file import write_array_to_wav
from utils.signals import test_signal, zeros, stack
from utils.plot import plot_signal
from evaluation import sabine_eyring_t60, calc_T60, truncate_list
from performance import Performance

# start total runtime and setup timers
total_performance = Performance()
setup_performance = Performance()

# setup the delay network
source_location = Point3(SOURCE_LOC[0], SOURCE_LOC[1], SOURCE_LOC[2])
mic_location = Point3(MIC_LOC[0], MIC_LOC[1], MIC_LOC[2])
room = Room(ROOM_DIMS, source_location, mic_location, ER_ORDER) 
sdn = Network(room.early_reflections, source_location, mic_location, WALL_ABSORPTION, FS, DIRECT_PATH) 
setup_time = setup_performance.get_time()

# input / output arrays
channels = 1
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

for s in range(len(signal_in)):
    # process the current sample
    sample = signal_in[s]
    sample_out = sdn.process(sample)  
    # model mic orientation with left right gain - use microphone array instead
    signal_out[s] = sample_out
    
    print(f"processing sample: {s}")

simulation_time = simulation_performance.get_time()
total_runtime = total_performance.get_time()
is_real_time, is_real_time_speedup = simulation_performance.is_real_time()

# show total run time
if TIMER:
    print(f"RUN TIME: {total_runtime} Secs")
    print(f"SETUP TIME: {setup_time} Secs")
    print(f"SIMULATION TIME: {simulation_time} Secs")
    print(f"IS REAL TIME: {is_real_time}")
    print(f"IS REAL TIME WITH 10x SPEEDUP: {is_real_time_speedup}")
    
# output the result
if OUTPUT_TO_FILE: 
    print("writing to file...")
    file_name = f"IR_junctions:{len(sdn.junctions)}_wall-attenuation:{WALL_ABSORPTION}_fs:{FS}_room:{ROOM_DIMS}_source:{SOURCE_LOC}_mic:{MIC_LOC}_order:{ER_ORDER}"
    write_array_to_wav(file_name, signal_out, FS)

# plot the result
if PLOT:
    print("plotting...")
    # get mono signal for evaluation       
    mono_in = signal_in
    rir = signal_out
    rir = truncate_list(rir)
    
    # get sabine / eyring T60 values
    sabine, eyring = sabine_eyring_t60(ROOM_DIMS, WALL_ABSORPTION)
    config_params = f"Room Dimensions: {ROOM_DIMS}, Source: {SOURCE_LOC}, Mic: {MIC_LOC}, Wall Absorption: {WALL_ABSORPTION} Order: {ER_ORDER}"
    plot_signal(rir / np.max(rir), title=config_params, xlim=[0.0,0.25])
    # plot_in_vs_out(mono_in, mono_out) # changed function name
    # plot_T60(mono_out, sabine, eyring, FS, title="T60 - " + config_params)
    # plot_frequnecy_response(mono_out, title=config_params)
    # # get model rt60 and compare to sabine and eyring
    model_t60 = calc_T60(rir, FS, sabine, plot=True)
    # print(model_t60, sabine)
    plt.show()