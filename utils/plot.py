import numpy as np
from matplotlib import pyplot as plt
from math import floor
from evaluation import truncate_list
from config import FS
from mpl_toolkits.mplot3d import Axes3D

def plot_signal(signal, title, xlim=None, fs=FS):
    time_vec = np.arange(signal.shape[0]) / fs
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal)
    plt.ylabel('Amplitude Linear')
    plt.xlabel('Samples')
    # if(xlim != None): plt.xlim(xlim)
    
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
# Function to plot the room and positions
def plot_room(room_dimensions, source_pos, mic_pos, reflections):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Room dimensions
    room_x, room_y, room_z = room_dimensions

    # Plot room
    # Creating the walls, floor, and ceiling
    ax.plot([0, room_x], [0, 0], [0, 0], color='k')
    ax.plot([0, room_x], [room_y, room_y], [0, 0], color='k')
    ax.plot([0, room_x], [0, 0], [room_z, room_z], color='k')
    ax.plot([0, room_x], [room_y, room_y], [room_z, room_z], color='k')
    ax.plot([0, 0], [0, room_y], [0, 0], color='k')
    ax.plot([room_x, room_x], [0, room_y], [0, 0], color='k')
    ax.plot([0, 0], [0, room_y], [room_z, room_z], color='k')
    ax.plot([room_x, room_x], [0, room_y], [room_z, room_z], color='k')
    ax.plot([0, 0], [0, 0], [0, room_z], color='k')
    ax.plot([room_x, room_x], [0, 0], [0, room_z], color='k')
    ax.plot([0, 0], [room_y, room_y], [0, room_z], color='k')
    ax.plot([room_x, room_x], [room_y, room_y], [0, room_z], color='k')

    # Plot source position
    ax.scatter(source_pos[0], source_pos[1], source_pos[2], color='r', label='Source')

    # Plot microphone position
    ax.scatter(mic_pos[0], mic_pos[1], mic_pos[2], color='b', label='Microphone')

    # Plot reflections
    reflections = np.array(reflections)
    if reflections.size > 0:
        ax.scatter(reflections[:, 0], reflections[:, 1], reflections[:, 2], color='g', label='Early Reflections')

    # Labels and limits
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_xlim([0, room_x])
    ax.set_ylim([0, room_y])
    ax.set_zlim([0, room_z])

    ax.legend()
    plt.show()