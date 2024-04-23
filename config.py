from math import floor

# constants
FS = 44100
SIGNAL_LENGTH = 44100
MAX_DELAY_SECS = 1.0
MAX_DELAY = floor(MAX_DELAY_SECS * FS)
SPEED_OF_SOUND = 343.0

# parameters
WALL_ABSORPTION = 0.25 # extend to be defined for each wall
ROOM_DIMS = [5,7,5]
SOURCE_LOC = [0.3, 0.5, 0.9]
MIC_LOC = [2.4, 2.1, 2.4]
CHANNEL_LEVELS = [1.0, 1.0] # left, right - use azimuth instead

# test signal
TEST_SIGNAL = "unit" # unit, noise, pulse, sample
BURST_LENGTH = 0.01

# outputs
OUTPUT_TO_FILE = False
PLOT = True