import numpy as np
from math import floor
from random import uniform

def unit_impulse(signal_length, gain=1.0):
    signal = zeros(signal_length)
    signal[0] = gain
    return signal

def noise_burst(signal_length, burst_secs, fs, gain=1.0):
    burst_samples = floor(burst_secs * fs)
    signal = zeros(signal_length)
    
    for i in range(0, burst_samples): 
        signal[i] = uniform(-gain, gain)
        gain -= 1 / burst_samples
    
    return signal
        
def zeros(length):
    return np.zeros(length, dtype=np.float32) 