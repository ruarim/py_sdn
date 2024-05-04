import numpy as np
from matplotlib import pyplot as plt
from math import floor

def plot_signal(signal, title):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal)
    plt.ylabel('Amplitude Linear')
    plt.xlabel('Samples')
    plt.show()
    
def plot_in_vs_out(signal_in, signal_out, title="Input vs Output signals"):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal_in, label='Input Signal')
    plt.plot(signal_out, label='Output Signal')
    plt.ylabel('Amplitude Linear')
    plt.xlabel('Samples')
    plt.legend()
    plt.show()
    
def plot_T60(signal_out, sabine_T60, eyring_T60, fs, title="T60"):
    signal_out_db = linear_to_dB(np.abs(signal_out))
    minus_60dB = max(signal_out_db) - 60 # ??
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal_out_db, label='Output Signal')
    plt.vlines(sabine_T60 * fs, ymin=min(signal_out_db), ymax=max(signal_out_db), color='g', linestyle='--', label='T60 Sabine: {} Secs'.format(sabine_T60))
    plt.vlines(eyring_T60 * fs, ymin=min(signal_out_db), ymax=max(signal_out_db), color='y', linestyle='--', label='T60 Eyring: {} Secs'.format(eyring_T60))
    plt.hlines(minus_60dB, xmin=0, xmax=len(signal_out_db), color='r', linestyle='--', label='-60dB: {}dB'.format(minus_60dB))
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

# normalised linear to dB conversion
def linear_to_dB(x):
    epsilon = 1e-20
    x_max = np.max(x)
    return 20 * np.log10((x + epsilon) / x_max)