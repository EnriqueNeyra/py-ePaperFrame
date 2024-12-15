import os
import sys
from PIL import Image
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
pic_path = os.path.join(script_dir, 'pic')
bmp_path = os.path.join(script_dir, 'bmp')
sys.path.append(pic_path)
sys.path.append(bmp_path)

class ImageConverter:

    def __init__(self):
        self.random = 0
        # self.image_files = [f for f in os.listdir('pic') if f.endswith(('.png', '.jpg', '.jpeg'))

    def process_images(self):
        # Take all images found in pic
        #
        return

    def to_bmp(self, input_jpg, output_path):
        # Resize image
        self.resize_image(input_jpg)

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
            0, 0, 0,  # Black
            85, 85, 85,  # Dark Gray
            170, 170, 170,  # Light Gray
            255, 255, 255  # White
        ]
        img_2bit.putpalette(palette)

        # Save as BMP
        img_2bit.save(output_path, format="BMP")

        return output_path

    def resize_image(self, path):
        # Screen target size dims
        target_width = 400
        target_height = 300

        with Image.open(path) as img:
            # Original dimensions
            orig_width, orig_height = img.size

            original_aspect_ratio = orig_width / orig_height
            target_aspect_ratio = target_width / target_height

            # Fit height and crop sides
            if original_aspect_ratio > target_aspect_ratio:
                new_height = target_height
                new_width = int(new_height * original_aspect_ratio)
            # Fit width and crop top/bottom
            else:
                new_width = target_width
                new_height = int(new_width / original_aspect_ratio)

            # Resize the image while maintaining aspect ratio
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Calculate the cropping box to center the crop
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height

            # Crop the image
            cropped_img = resized_img.crop((left, top, right, bottom))

            # Save the final image
            cropped_img.save(path)

    @staticmethod
    def to_bmp_auto(input_jpg, output_path):
        # Read the image
        img = Image.open(input_jpg).convert("L")  # Convert to grayscale

        # Map grayscale levels to 2-bit levels (0, 1, 2, 3)
        # Four levels: 0 -> 0, 64 -> 1, 128 -> 2, 192 -> 3
        img_array = np.array(img)
        img_2bit = (img_array // 64).clip(0, 3) * 85

        # Convert back to an image
        img_2bit_image = Image.fromarray(img_2bit.astype("uint8"))

        # Save as BMP
        img_2bit_image.save(output_path, format="BMP")

        return output_path