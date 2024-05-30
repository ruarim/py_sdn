# contains delay from course to junctions and microphone
from utils.vec3 import Vec3
from propigation_line import PropigationLine

class Source:     
    def __init__(self, location: Vec3):
        self.propigation_lines: list[PropigationLine] = [] # source -> junction
        self.direct_path: PropigationLine = None # source -> mic
        self.location: Vec3 = location
    
    def add_to_junction(self, prop_line: PropigationLine):
        self.propigation_lines.append(prop_line)
        
    def add_direct_path(self, prop_line: PropigationLine):
        self.direct_path = prop_line