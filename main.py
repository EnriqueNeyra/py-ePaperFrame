import os
import sys
import cv2
import time
import numpy as np
# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
pic_path = os.path.join(script_dir, 'pic')
sys.path.append(lib_path)
from waveshare_epd import epd4in2_V2

epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()

epd.Init_4Gray()
Himage = cv2.imread(os.path.join(pic_path, 'imageColor.bmp'))
epd.display_4Gray(epd.getbuffer_4Gray(Himage))
time.sleep(4)

epd.Clear()


def process_image():
    # Read the image
    img = cv2.imread('pic/image.jpg')

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Quantize to 2-bit grayscale (4 levels)
    n = gray.size
    data = gray.flatten()

    # Quantize pixel values to 4 levels
    for i in range(n):
        pixel_value = data[i]
        if pixel_value < 64:
            data[i] = 0  # Black: 00
        elif pixel_value < 128:
            data[i] = 1  # Dark Gray: 01
        elif pixel_value < 192:
            data[i] = 2  # Light Gray: 10
        else:
            data[i] = 3  # White: 11

    # Constants for width and height
    width, height = 400, 300

    # Calculate size of compressed data and allocate memory for the compressed data
    image_size = ((width % 8 == 0) and (width // 4) or (width // 4 + 1)) * height

    compressed_data = np.zeros(image_size, dtype=np.uint8)

    # Compress data into 4 pixels per byte
    ci = 0
    for i in range(0, n, 4):
        com = data[i]  # Start with the first pixel
        com = (com << 2) | data[i + 1]  # Shift by 2 bits and OR with the second pixel
        com = (com << 2) | data[i + 2]  # Shift by 2 bits and OR with the third pixel
        com = (com << 2) | data[i + 3]  # Shift by 2 bits and OR with the fourth pixel
        compressed_data[ci] = com  # Store the byte in the compressed data array
        ci += 1  # Move to the next byte in compressed_data

    # compressed_data now contains the compressed image data
    print([f"0x{byte:02x}" for byte in compressed_data[:10]])
