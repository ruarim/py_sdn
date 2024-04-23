from scipy.io.wavfile import write
from datetime import datetime
from matplotlib import pyplot as plt

# add read file for processing function

def write_array_to_wav(file_name: str, audio_data, fs):
    # add create output folder if it does not exist
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
