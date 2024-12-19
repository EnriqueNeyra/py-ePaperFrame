import os
import sys

# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
sys.path.append(lib_path)
from waveshare_epd import epd5in65f

epd = epd5in65f.EPD()
epd.init()
epd.Clear()
epd.sleep()

