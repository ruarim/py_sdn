import numpy as np
from math import floor
from random import uniform
from utils import read_wav_file

def zeros(length):
    return np.zeros(length, dtype=np.float32) 

# generate a unit impulse
def unit_impulse(signal_length, gain):
    signal = zeros(signal_length)
    signal[0] = gain
    return signal

# generate a noise burst
def noise_burst(signal_length, burst_secs, fs, gain):
    burst_samples = floor(burst_secs * fs)
    signal = zeros(signal_length)
    
    for i in range(0, burst_samples): 
        signal[i] = uniform(-gain, gain)
        gain -= 1 / burst_samples
    
    return signal

# read a sample file
def file(data_dir, file_name):
    fs, data = read_wav_file(data_dir, file_name)
    return data

# return fs depenant on signal type 
def test_signal(choice, signal_length, fs,burst_secs=0.1, gain=1.0, data_dir="", file_name=""):
    if choice == "unit": return unit_impulse(signal_length, gain)
    if choice == "noise": return noise_burst(signal_length, burst_secs, fs, gain)
    if choice == "file": return file(data_dir, file_name) # not returning fs for now
    # if "pulse": return pulse with harmonic content (sine, square, tri...)

def signal_duplicator(signal):
    n = 2   
    return np.column_stack([signal] * n)