from time import perf_counter

class Performance:
    def __init__(self):
        self.start_time = perf_counter()
        
    def time(self):
        self.stop_time = perf_counter()
        return self.stop_time - self.start_time