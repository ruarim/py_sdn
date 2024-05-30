# defines the geometry of a room
# and its frequency dependant and independant wall absorption coefficients

from utils.vec3 import Vec3
from early_reflections import find_reflections

class Room:
    def __init__(self, dims: list[float], source: Vec3, mic: Vec3): 
        # only shoebox for now        
        self.dims = dims
        self.valid_shape()
        self.source = source
        self.mic = mic
        self.valid_source_mic()
        self.early_reflections = find_reflections(self.dims, self.source) # inject instead?
        
        # wall filter coefficient
        
        # wall attenuation values
        
    
    def valid_shape(self):
        assert all(dim > 0 for dim in self.dims), "invalid room shape"
    
    def valid_source_mic(self):
        assert self.source.less_than(self.dims[0], self.dims[1], self.dims[2])
        assert self.mic.less_than(self.dims[0], self.dims[1], self.dims[2])
    
    def update_reflections(self):
        self.early_reflections = find_reflections(self.dims, self.source)