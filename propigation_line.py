# prop path: A unidirectional delayline containing all the operations between two connected scattering nodes.
# 
#                                  --[wall filter]->[send sample to receiver]->[delay]->[add-sample from source]-->
#             <scattering junction>                                                                                 <scattering junction>
#                                  <--[add sample from source]<-[delay]<-[send sample to receiver]<-[wall filter]--
from utils.delay_line import DelayLine
from config import FS, SPEED_OF_SOUND
from utils.point3 import Point3
from math import sqrt, floor

# currently adding typing to this class is limited by circular imports
# possibly create types / interfaces module
class PropigationLine:    
    def __init__(self, start, end, fs=FS, c=SPEED_OF_SOUND, offset=0):
        self.fs = fs
        self.c = c
        self.delay_line = DelayLine()
        self.start = start
        self.end = end
        self.distance = self.euclid_dist()
        self.offset = offset
        self.attenuation = 1.0
        
        # filter for frequnecy dependant air absorption
            
    def sample_in(self, sample: float):
        self.delay_line.push(sample)
        
    def sample_out(self) -> float:
        delay = self.distance_to_delay()
        return self.delay_line.read(delay + self.offset) * self.attenuation 
    
    # get the euclidean distance between the start and end junctions
    def euclid_dist(self):
        diff = self.vector_diff(self.start.location, self.end.location)
        distance = sqrt(diff.x**2 + diff.y**2 + diff.z**2)
        return distance
    
    # convert the distance to a delay in samples
    def distance_to_delay(self):
        return floor(self.fs * (self.distance / self.c))
    
    def vector_diff(self, point_a: Point3, point_b: Point3): 
        x_diff = point_a.x - point_b.x
        y_diff = point_a.y - point_b.y
        z_diff = point_a.z - point_b.z
        return Point3(x_diff, y_diff, z_diff)
    
    # def update_distance()