from PIL import Image
import numpy as np


class ImageConverter:

    @staticmethod
    def process_image(input_jpg, output_path):
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

    @staticmethod
    def to_bmp(input_jpg, output_path):
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