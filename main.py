import os
import sys
import time
from PIL import Image
from image_converter import ImageConverter

# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
sys.path.append(lib_path)
from waveshare_epd import epd5in65f

def main():
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()

    converter = ImageConverter()
    converter.process_images()

    # List of all image files in output directory
    image_files = [f for f in os.listdir(converter.output_directory)]

    while True:
        for filename in image_files:
            filepath = os.path.join(converter.output_directory, filename)

            # Open and display the image
            with Image.open(filepath) as bmp_img:
                bmp_img = bmp_img.rotate(180)
                epd.display(epd.getbuffer(bmp_img))

            # Sleep for 30 minutes (1800 seconds) between each image
            time.sleep(900)  # 30 minutes

    # epd.init()
    # epd.Clear()
    # epd.sleep()

if __name__ == "__main__":
    main()


