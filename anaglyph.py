#!/usr/bin/env python3
"""
create_anaglyph.py

This script creates a red–cyan anaglyph image from a single input image
or from all images in an input directory.

For a single image:
    python create_anaglyph.py input_image.jpg output_anaglyph.jpg [offset]

For a directory of images:
    python create_anaglyph.py input_directory output_directory [offset]

Arguments:
    input_image.jpg or input_directory
         Path to the input image file or directory containing images.
    output_anaglyph.jpg or output_directory
         Path where the output image or images will be saved.
    offset (optional)
         Horizontal shift in pixels (default is 10).

Dependencies:
    Pillow (install via pip: pip install pillow)
"""

import sys
import os
from PIL import Image, ImageChops

def create_anaglyph(input_path, output_path, offset=10):
    """
    Create a red–cyan anaglyph image from a single input image.
    
    Parameters:
        input_path (str): Path to the input image.
        output_path (str): Path where the anaglyph image will be saved.
        offset (int): Horizontal shift applied to the red channel.
    """
    try:
        img = Image.open(input_path).convert("RGB")
    except Exception as e:
        print(f"Error opening {input_path}: {e}")
        return False

    # Create a left view by shifting the image to the left.
    left_img = ImageChops.offset(img, -offset, 0)
    
    # Extract the red channel from the left image.
    left_red = left_img.split()[0]
    
    # Use the original image's green and blue channels for the right view.
    right_green, right_blue = img.split()[1], img.split()[2]
    
    # Merge channels to create the red-cyan anaglyph.
    anaglyph = Image.merge("RGB", (left_red, right_green, right_blue))
    
    try:
        anaglyph.save(output_path)
        print(f"Anaglyph saved as {output_path}")
        return True
    except Exception as e:
        print(f"Error saving {output_path}: {e}")
        return False

def process_directory(input_dir, output_dir, offset=10):
    """
    Process all image files in the input directory and create anaglyphs.
    
    Parameters:
        input_dir (str): Path to the directory with input images.
        output_dir (str): Directory where output images will be saved.
        offset (int): Horizontal shift applied to the red channel.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # List of allowed image file extensions.
    allowed_ext = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    for filename in os.listdir(input_dir):
        file_lower = filename.lower()
        _, ext = os.path.splitext(file_lower)
        if ext in allowed_ext:
            input_file = os.path.join(input_dir, filename)
            base, ext_original = os.path.splitext(filename)
            output_file = os.path.join(output_dir, f"{base}_anaglyph{ext_original}")
            create_anaglyph(input_file, output_file, offset)
        else:
            print(f"Skipping non-image file: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_anaglyph.py input_image_or_directory output_image_or_directory [offset]")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    offset_val = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    # If the input is a directory, ensure the output is also a directory.
    if os.path.isdir(input_path):
        if not os.path.isdir(output_path):
            print("Error: When input is a directory, output must also be a directory.")
            sys.exit(1)
        process_directory(input_path, output_path, offset_val)
    else:
        create_anaglyph(input_path, output_path, offset_val)
