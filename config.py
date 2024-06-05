from math import floor

# constants
FS = 44100
SIGNAL_LENGTH = 22050
MAX_DELAY_SECS = 1.0
MAX_DELAY = floor(MAX_DELAY_SECS * FS)
SPEED_OF_SOUND = 343.0

# parameters
WALL_ABSORPTION = 0.25 # extend to be defined for each wall
ROOM_DIMS = [5, 7, 5] # x, y, z - length, width, height
SOURCE_LOC = [3.4, 3.1, 3.4] # place in center for evaluation - same below
MIC_LOC = [2.4, 2.1, 2.4]
CHANNEL_LEVELS = [1.0, 1.0] # left, right - use azimuth instead
DIRECT_PATH=True
ER_ORDER=1

# test signal
TEST_SIGNAL = "unit" # unit, noise, pulse, file
BURST_LENGTH = 0.01
DATA_DIR = "_samples/"
FILE_NAME = "Clap 808 Color 03.wav"

# outputs
OUTPUT_TO_FILE = True
PLOT = True
TIMER = False