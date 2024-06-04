import numpy as np
from matplotlib import pyplot as plt
from math import floor
from evaluation import truncate_list
from config import FS

def plot_signal(signal, title, xlim=None, fs=FS):
    time_vec = np.arange(signal.shape[0]) / fs
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(time_vec, signal)
    plt.ylabel('Amplitude Linear')
    plt.xlabel('Samples')
    if(xlim != None): plt.xlim(xlim)
    
def plot_compare(signals, signals_labels, title="Input vs Output signals"):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    for i in range(signals):
        plt.plot(signals[i], label=signals_labels[i])
    plt.ylabel('Amplitude Linear')
    plt.xlabel('Samples')
    plt.legend()
    
def plot_T60(h, sabine_T60, eyring_T60, fs, title="T60"):
    h_db = linear_to_dB_norm(np.abs(truncate_list(h)))
    minus_60dB = max(h_db) - 60
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(h_db, label='Output Signal')
    plt.vlines(sabine_T60 * fs, ymin=min(h_db), ymax=max(h_db), color='g', linestyle='--', label='T60 Sabine: {} Secs'.format(sabine_T60))
    plt.vlines(eyring_T60 * fs, ymin=min(h_db), ymax=max(h_db), color='y', linestyle='--', label='T60 Eyring: {} Secs'.format(eyring_T60))
    plt.hlines(minus_60dB, xmin=0, xmax=len(h_db), color='r', linestyle='--', label='-60dB: {}dB'.format(minus_60dB))
    plt.ylabel('Amplitude (Normalised dB)')
    plt.xlabel('Samples')
    plt.legend()

def plot_frequnecy_response(y, title):
    X = linear_to_dB_norm(np.abs(np.fft.fft(y)))
    half_X = floor(len(X)/2)
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(X[:half_X])
    plt.ylabel('Magnitude (Normalised dB)')
    plt.xlabel('Frequency')

# normalised linear to dB conversion
def linear_to_dB_norm(x):
    epsilon = 1e-20
    x_max = np.max(x)
    return 20 * np.log10((x + epsilon) / x_max)

# plot room dimension, source, mic, reflections