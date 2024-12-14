import os
import sys
import time
import numpy as np
from PIL import Image
from image_converter import ImageConverter
# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
pic_path = os.path.join(script_dir, 'pic')
sys.path.append(lib_path)
from waveshare_epd import epd4in2_V2

def process_image(input_jpg, output_path):
    # Read the image
    img = Image.open(input_jpg).convert("L") # Convert to grayscale

    # Map grayscale levels to 2-bit levels (0, 1, 2, 3)
    # Four levels: 0 -> 0, 64 -> 1, 128 -> 2, 192 -> 3
    img_array = np.array(img)
    img_2bit = (img_array // 64).clip(0, 3) * 85

    # Convert back to an image
    img_2bit_image = Image.fromarray(img_2bit.astype("uint8"))

    # Save as BMP
    img_2bit_image.save(output_path, format="BMP")

    return output_path

def manual_process_image(input_jpg, output_path):
    # Open image
    img = Image.open(input_jpg).convert("L")  # Convert to grayscale

    array_orig = np.array(img)
    array_flat = array_orig.ravel()

    # Quantize pixel values to 4 levels
    n = img.width * img.height
    for i in range(n):
        pixel_value = array_flat[i]
        if pixel_value < 64:
            array_flat[i] = 0  # Black: 00
        elif pixel_value < 128:
            array_flat[i] = 1  # Dark Gray: 01
        elif pixel_value < 192:
            array_flat[i] = 2  # Light Gray: 10
        else:
            array_flat[i] = 3  # White: 11

    # Reverse array flattening
    array_2bpp = array_flat.reshape(array_orig.shape)

    # Create a new image in "P" mode (palette-based)
    img_2bit = Image.fromarray(array_2bpp, mode="P")

    # Define a grayscale palette for 2-bit levels
    palette = [
        0, 0, 0,      # Black
        85, 85, 85,   # Dark Gray
        170, 170, 170,  # Light Gray
        255, 255, 255  # White
    ]
    img_2bit.putpalette(palette)

    # Save as BMP
    img_2bit.save(output_path, format="BMP")

    return output_path

epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()

epd.Init_4Gray()

bmp_image_path = ImageConverter.to_bmp('pic/image.jpg', 'pic/image.bmp')
BMPImage1 = Image.open(bmp_image_path)
buf2 = epd.getbuffer_4Gray(BMPImage1)
epd.display_4Gray(epd.getbuffer_4Gray(BMPImage1))
time.sleep(5)

epd.init()
epd.Clear()
epd.sleep()



