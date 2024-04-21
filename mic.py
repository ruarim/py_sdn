# contains the delay from junctions to microphone
# and models microphone pattern

from point_3D import Point3D
from propigation_line import PropigationLine

# source and mic are very similar and could be refactored
class Mic:  
    def __init__(self, location: Point3D):
        self.propigation_lines = [] # junction -> mic
        self.direct_path = None # source -> mic
        self.location = location
    
    def add_from_junction(self, prop_line: PropigationLine):
         # should be call outside this function - junction needs access?
        self.propigation_lines.append(prop_line)
    
    def add_direct_path(self, prop_line: PropigationLine):
        self.direct_path = prop_line
    