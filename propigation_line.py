# prop path: A unidirectional delayline containing all the operations between two connected scattering nodes.
# 
#                                  --[wall filter]->[send sample to receiver]->[delay]->[add-sample from source]-->
#             <scattering junction>                                                                                 <scattering junction>
#                                  <--[add sample from source]<-[delay]<-[send sample to receiver]<-[wall filter]--
from delay_line import DelayLine
from config import FS, SPEED_OF_SOUND
from point_3D import Point3D
from math import sqrt, floor
from utils import clamp

# currently adding typing to this class is limited by circular imports
# possibly create types / interfaces module
class PropigationLine:    
    def __init__(self, start, end, fs=FS, c=SPEED_OF_SOUND, absorbing=False):
        self.fs = fs
        self.c = c
        self.delay_line = DelayLine()
        self.start = start
        self.end = end
        self.distance = self.euclid_dist()
        self.attenuation = 1.0
        
        # apply attenuation to source, mic and direct path proplines only
        if(absorbing):
            # (1 + (junction mic distance / source junction distance))
            self.attenuation = clamp(1 / self.distance, 0, 1)
        
        # filter for frequnecy dependant absorption
            
    def sample_in(self, sample: float):
        self.delay_line.push(sample)
        
    def sample_out(self) -> float:
        delay = self.distance_to_delay()
        return self.delay_line.read(delay) * self.attenuation 
    
    def set_attenuation(self):
        pass
        
    # get the euclidean distance between the start and end junctions
    def euclid_dist(self):
        diff = self.vector_diff(self.start.location, self.end.location)
        distance = sqrt(diff.x**2 + diff.y**2 + diff.z**2)
        return distance
    
    # convert the distance to a delay in samples
    def distance_to_delay(self):
        return floor(self.fs * (self.distance / self.c))
    
    def vector_diff(self, point_a: Point3D, point_b: Point3D): 
        x_diff = point_a.x - point_b.x
        y_diff = point_a.y - point_b.y
        z_diff = point_a.z - point_b.z
        return Point3D(x_diff, y_diff, z_diff)
    
    # def update_distance()