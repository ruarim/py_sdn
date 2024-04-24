from scipy.io.wavfile import write, read
import scipy.io
from datetime import datetime
from matplotlib import pyplot as plt
from os import path 
import numpy as np
import warnings

def read_wav_file(data_dir: str, file_name: str): 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", scipy.io.wavfile.WavFileWarning)
        
        # construct the path to the WAV file.
        wav_fname = path.join(data_dir, file_name)

        # read the WAV file.
        fs, data = scipy.io.wavfile.read(wav_fname)
    
    # determine the bit depth of the data and normalize it to the range [-1, 1].
    if data.dtype == np.int16:
        data = data.astype(np.float32) / np.iinfo(np.int16).max
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / np.iinfo(np.int32).max
    elif data.dtype == np.uint8:  # 8-bit WAV files are usually unsigned
        data = (data.astype(np.float32) - 128) / np.iinfo(np.uint8).max  # adjusting range to [-1, 1]
    
    return fs, data

def write_array_to_wav(file_name: str, audio_data, fs):
    date_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    output_file = f'_output/{date_time}-{file_name}.wav'
    write(output_file, fs, audio_data)
    
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def plot_signal(signal, title):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal)
    plt.show()
    
def plot_in_vs_out(signal_in, signal_out, title="Input vs Output signals"):
    plt.figure(figsize=(10, 4))
    plt.title(title)
    plt.plot(signal_in, label='Input Signal')
    plt.plot(signal_out, label='Output Signal')
    plt.legend()
    plt.show()
