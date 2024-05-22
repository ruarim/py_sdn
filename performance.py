from time import perf_counter
from config import FS, SIGNAL_LENGTH

class Performance:
    def __init__(self, fs=FS, buffer_size=SIGNAL_LENGTH ):
        self.start_time = perf_counter()
        self.threshold = buffer_size / fs
        
        # instead use dict of times eg, times["total"]
        
    def get_time(self):
        self.stop_time = perf_counter()
        self.time = (self.stop_time - self.start_time)
        return self.time
    
    def is_real_time(self):
        standard = False
        speedup_10x = False
        if self.threshold > self.time: standard = True
        if self.threshold > self.time / 10: speedup_10x = True
        
        return standard, speedup_10x
        