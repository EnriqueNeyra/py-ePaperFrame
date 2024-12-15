import os
import sys
import time
from PIL import Image
from image_converter import ImageConverter

# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
sys.path.append(lib_path)
from waveshare_epd import epd4in2_V2

def main():
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    epd.Init_4Gray()

    converter = ImageConverter()
    converter.process_images()
    for filename in os.listdir(converter.output_directory):
        filepath = os.path.join(converter.output_directory, filename)

        with Image.open(filepath) as bmp_img:
            epd.display_4Gray(epd.getbuffer_4Gray(bmp_img))
            time.sleep(5)

    epd.init()
    epd.Clear()
    epd.sleep()

if __name__ == "__main__":
    main()


