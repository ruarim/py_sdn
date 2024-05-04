import numpy as np
from matplotlib import pyplot as plt
from math import floor

def plot_signal(signal, title):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal)
    plt.ylabel('Amplitude Linear') # units
    plt.xlabel('Samples')
    plt.show()
    
def plot_in_vs_out(signal_in, signal_out, T60, fs, title="Input vs Output signals"):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    # plt.plot(np.abs(signal_in), label='Input Signal')
    signal_out_db = linear_to_dB(np.abs(signal_out))
    plt.plot(signal_out_db, label='Output Signal')
    plt.vlines(T60 * fs, ymin=min(signal_out_db), ymax=max(signal_out_db), color='g', linestyle='--', label='T60: {} Secs'.format(T60))
    plt.ylabel('Amplitude (dB)')
    plt.xlabel('Samples')
    plt.legend()
    plt.show()

def plot_frequnecy_response(y, title):
    X = linear_to_dB(np.abs(np.fft.fft(y)))
    half_X = floor(len(X)/2)
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(X[:half_X])
    plt.ylabel('Magnitude (dB)')
    plt.xlabel('Frequency')
    plt.show()

def linear_to_dB(x):
    epsilon = 1e-20
    # x = np.maximum(x, epsilon)
    x_max = np.max(x)
    return 20 * np.log10((x + epsilon) / x_max)