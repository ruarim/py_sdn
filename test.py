from utils import read_wav_file

samples_dir = '_samples/'
file_name = 'Clap 808 Color 03.wav'
fs, data, = read_wav_file(samples_dir, file_name)

data = data[0:]
print(fs, data)

import matplotlib.pyplot as plt
import numpy as np

length = data.shape[0] / fs
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data, label="Left channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()