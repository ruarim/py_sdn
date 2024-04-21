# contains delay from course to junctions and microphone
from point_3D import Point3D
from propigation_line import PropigationLine

class Source:     
    def __init__(self, location: Point3D):
        self.propigation_lines = [] # source -> junction
        self.direct_path = None # source -> mic
        self.location = location
    
    def add_to_junction(self, prop_line: PropigationLine):
        self.propigation_lines.append(prop_line)
        
    def add_direct_path(self, prop_line: PropigationLine):
        self.direct_path = prop_line