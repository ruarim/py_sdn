# prop path: A unidirectional delayline containing all the operations between two connected scattering nodes.
# 
#                                  --wall filter->send sample to receiver->delay->add-sample from source-->
#             <scattering junction>                                                                        <scattering junction>
#                                  <--add sample from source<-delay<-send sample to receiver<-wall filter--
from delay_line import DelayLine
from constants import MAX_DELAY

# currently adding typing to this class is limited by circular imports
# possibly create types / interfaces module
class PropigationLine:    
    def __init__(self, start, end):
        self.distance = "vector difference between start and end"
        self.delay_line = DelayLine(MAX_DELAY)
        self.start = start
        self.end = end
        
        # aborbing filter ?
        # air aborption  ?
            
    def sample_in(self, sample):
        self.delay_line.push(sample)
        
    def sample_out(self):
        return self.delay_line.read(self.distance)