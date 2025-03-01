from PIL import Image
from pillow_heif import register_heif_opener
import os


def convert_to_baseline_jpeg(input_image_path, output_image_path):
    with Image.open(input_image_path) as img:
        baseline_jpeg = img.convert("RGB")
        baseline_jpeg.save(output_image_path, "JPEG", quality=100, optimize=True, baseline=True)

def convert_to_progressive_jpeg(input_image_path, output_image_path):
    with Image.open(input_image_path) as img:
        progressive_jpeg = img.convert("RGB")
        progressive_jpeg.save(output_image_path, "JPEG", quality=100, optimize=True, progressive=True)

def convert_to_png(input_image_path, output_image_path):
    with Image.open(input_image_path) as img:
        img.save(output_image_path, "PNG", optimize=True)

def valid_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width <= 8192 and height <= 8192

def batch_convert(input_directory, output_directory, output_format, wii_photo_channel_size_limit):
    if not os.path.exists(input_directory):
        os.makedirs(input_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".heic", ".heif"}

    for filename in os.listdir(input_directory):

        register_heif_opener()

        input_image_path = os.path.join(input_directory, filename)

        if not os.path.isfile(input_image_path):
            continue

        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension not in image_extensions:
            continue

        if wii_photo_channel_size_limit and not valid_image_size(input_image_path):
            continue

        if output_format == "PNG":
            output_file_extension = ".png"
        else:
            output_file_extension = ".jpeg"

        if file_extension in ['.heic', '.heif']:
            heic_image = Image.open(input_image_path)
            input_image_path = os.path.splitext(input_image_path)[0] + output_file_extension
            heic_image.save(input_image_path, format=output_file_extension[1:])

        output_image_path = os.path.join(output_directory, os.path.splitext(filename)[0] + output_file_extension)

        if os.path.exists(output_image_path):
            base_name = os.path.splitext(filename)[0]
            counter = 1
            while os.path.exists(os.path.join(output_directory, f"{base_name}_{counter}{output_file_extension}")):
                counter += 1
            output_image_path = os.path.join(output_directory, f"{base_name}_{counter}{output_file_extension}")

        if output_format == "JPEG Baseline":
            convert_to_baseline_jpeg(input_image_path, output_image_path)
        elif output_format == "JPEG Progressive":
            convert_to_progressive_jpeg(input_image_path, output_image_path)
        else:
            convert_to_png(input_image_path, output_image_path)

        # delete the temp png or jpeg from input folder
        if file_extension in ['.heic', '.heif']:
            os.remove(input_image_path)
