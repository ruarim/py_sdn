class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def less_than(self, x, y, z):
        return self.x < x and self.y < y and self.z < z
    