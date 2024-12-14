import os
import sys
import time
import numpy as np
from PIL import Image
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
    img_2bit = (img_array // 64).clip(0, 3) * 64

    # Convert back to an image
    img_2bit_image = Image.fromarray(img_2bit.astype("uint8"))

    # Save as BMP
    img_2bit_image.save(output_path, format="BMP")
    print(f"Saved 2-bit BMP to {output_path}")
    return output_path

#### OLD METHOD, MANUAL BIT MANIPULATION, NEEDS TESTING ####
def manual_process_image(input_jpg):
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
    img_2bpp = array_flat.reshape(array_orig.shape)

    # Convert back to an image
    img_2bit_image = Image.fromarray(img_2bpp.astype("uint8"))

    # Save as BMP
    img_2bit_image.save('pic/test.bmp', format="BMP")

    # # Constants for width and height
    # width, height = 400, 300
    #
    # # Calculate size of compressed data and allocate memory for the compressed data
    # image_size = ((width % 8 == 0) and (width // 4) or (width // 4 + 1)) * height
    #
    # compressed_data = np.zeros(image_size, dtype=np.uint8)
    #
    # # Compress data into 4 pixels per byte
    # ci = 0
    # for i in range(0, n, 4):
    #     com = data[i]  # Start with the first pixel
    #     com = (com << 2) | data[i + 1]  # Shift by 2 bits and OR with the second pixel
    #     com = (com << 2) | data[i + 2]  # Shift by 2 bits and OR with the third pixel
    #     com = (com << 2) | data[i + 3]  # Shift by 2 bits and OR with the fourth pixel
    #     #compressed_data[ci] = com  # Store the byte in the compressed data array
    #     compressed_data[ci] = com
    #     ci += 1  # Move to the next byte in compressed_data
    #
    # # Convert back to an image
    # compressed_data = compressed_data.reshape(height, int(image_size / height))
    #
    # return compressed_data

epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()

epd.Init_4Gray()

BMPImage = Image.open(process_image('pic/image.jpg', 'pic/image.bmp'))
buf = epd.getbuffer_4Gray(BMPImage)
print(len(buf))
print(type(buf))
print([f"0x{byte:02x}" for byte in buf[-10:]])
epd.display_4Gray(epd.getbuffer_4Gray(BMPImage))
time.sleep(5)
epd.display_4Gray(manual_process_image('pic/image.jpg'))
time.sleep(5)

epd.init()
epd.Clear()
epd.sleep()



