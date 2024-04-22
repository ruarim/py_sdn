import numpy as np
from point_3D import Point3D
from source import Source
from mic import Mic

class ScatteringJunction:    
    # add arg types
    def __init__(self, location: Point3D, source: Source, mic: Mic, wall_attenuation=1.0):
        self.propigation_in = []
        self.propigation_out = []
        self.location = location
        self.source = source
        self.mic = mic
        self.wall_attenuation = wall_attenuation
        
        # wall filter
    
    def scatter_out(self, source_sample):
        # get reflection order
        M = len(self.propigation_out)
        # samples in from neighbours
        samples_in = [s.sample_out() for s in self.propigation_in]
        sample_to_mic = 0.0
        samples_out = np.zeros(M)
        
        # for each prop out
        for i in range(M):
            prop_out = self.propigation_out[i]
            sample_out = 0.0
             # for each prop in
            for j in range(M):
                sample_in = samples_in[j] + (source_sample / 2)
                prop_in = self.propigation_in[j]
                # isotropic scattering coefficient
                # if out == in
                if i == j: a = 2 / M - 1.0 # less to diagonal
                else: a = 2 / M
                
                sample_out += sample_in * a
                            
            # filter sample (frequnecy dependant absorption) and attenuation (non frequency dependant absorption)
            
            # to neighbour junctions
            samples_out[i] = sample_out * self.wall_attenuation
                       
            # to mic prop line
            sample_to_mic += (2/M)*sample_out
                    
        return samples_out, sample_to_mic
    
    def scatter_in(self, samples):
        M = len(self.propigation_in)
        for i in range(M):
            self.propigation_in[i].sample_in(samples[i])
    
    def add_in(self, prop_in):
        self.propigation_in.append(prop_in)
        
    def add_out(self, prop_out):
        self.propigation_out.append(prop_out)
        
        
       