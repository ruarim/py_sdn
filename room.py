from point_3D import Point3D
# defines the geometry of a room

class Room:
    def __init__(self, x: float, y: float, z: float, source: Point3D, mic: Point3D): 
        # only shoebox for now        
        self.x = x
        self.y = y
        self.z = z
        self.valid_shape()
        
        self.source = source
        self.mic    = mic
        self.valid_source_mic()
        
        # wall filters
        # wall attenuation
    
    def valid_shape(self):
        assert self.x > 0 and self.y > 0 and self.z > 0, "invalid room shape"
    
    def valid_source_mic(self):
        assert self.source.less_than(self.x, self.y, self.z)
        assert self.mic   .less_than(self.x, self.y, self.z)