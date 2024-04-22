from scipy.io.wavfile import write
from datetime import datetime

def write_array_to_wav(file_name: str, audio_data, fs):
    # add create output folder if it does not exist
    date_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    output_file = f'output/{file_name}-{date_time}.wav'
    write(output_file, fs, audio_data)