import os
import sys
from PIL import Image, ImageEnhance
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
pic_path = os.path.join(script_dir, 'pic')
bmp_path = os.path.join(script_dir, 'bmp')
sys.path.append(pic_path)
sys.path.append(bmp_path)

class ImageConverter:

    def __init__(self):
        self.input_directory = pic_path
        self.output_directory = bmp_path

        os.makedirs(self.output_directory, exist_ok=True)

        self.image_files = [file for file in os.listdir('pic') if 'modified' not in file]

    def process_images(self):
        for file_name in self.image_files:
            original_img_path = os.path.join(self.input_directory, file_name)
            new_img_name = os.path.splitext(file_name)[0] + "_modified"
            modified_img_path = os.path.join(self.input_directory, new_img_name + os.path.splitext(file_name)[1])
            output_bmp_path = os.path.join(self.output_directory, new_img_name + ".bmp")

            self.resize_image(original_img_path, modified_img_path)
            os.remove(original_img_path)
            self.to_bmp_seven_color(modified_img_path, output_bmp_path)

    # Resize the image given by input_path and overwrite to the same path
    def resize_image(self, input_path, output_path):
        # Screen target size dims
        target_width = 600
        target_height = 448

        with Image.open(input_path) as img:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            
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
            cropped_img.save(output_path)
    
    # Convert input image to bmp and save at the specified output path
    def to_bmp_seven_color(self, input_path, output_path):
        # Define the 7 colors in the palette (RGB values)
        palette_colors = [
            (0, 0, 0),  # Black: 0x0
            (255, 255, 255),  # White: 0x1
            (0, 255, 0),  # Green: 0x2
            (0, 0, 255),  # Blue: 0x3
            (255, 0, 0),  # Red: 0x4
            (255, 255, 0),  # Yellow: 0x5
            (255, 165, 0)  # Orange: 0x6
        ]

        # Create the flat palette by expanding each color tuple into individual RGB values
        flat_palette = []
        for color in palette_colors:
            flat_palette.extend(color)

        # Pad the palette with zeros to make it 256 colors (each with 3 channels: RGB)
        remaining_colors = 256 - len(palette_colors)
        flat_palette.extend([0] * remaining_colors * 3)

        # Create a palette image with the 7 colors
        palette_img = Image.new("P", (1, 1))
        palette_img.putpalette(flat_palette)

        # Open the image and convert it to RGB
        img = Image.open(input_path).convert("RGB")

        # Quantize the input image using the palette
        img_quantized = img.quantize(palette=palette_img)

        # Save the quantized image as BMP
        img_quantized.save(output_path, format="BMP")

        return output_path
    
    # Convert input image to bmp and save at the specified output path
    def to_bmp_four_gray(self, input_path, output_path):
        # Open image
        img = Image.open(input_path).convert("L")  # Convert to grayscale

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
