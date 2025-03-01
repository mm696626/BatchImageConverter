from PIL import Image
from pillow_heif import register_heif_opener
import os


def convert_to_baseline_jpeg(input_image_path, output_image_path):
    with Image.open(input_image_path) as img:
        rgb_img = img.convert("RGB")
        rgb_img.save(output_image_path, "JPEG", quality=100, optimize=True, baseline=True)

def valid_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width <= 8192 and height <= 8192

def batch_convert(input_directory, output_directory):
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

        if not valid_image_size(input_image_path):
            continue

        if file_extension in ['.heic', '.heif']:
            heic_image = Image.open(input_image_path)
            input_image_path = os.path.splitext(input_image_path)[0] + ".jpeg"
            heic_image.save(input_image_path, format="jpeg")

        output_image_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".jpg")

        if os.path.exists(output_image_path):
            base_name = os.path.splitext(filename)[0]
            counter = 1
            while os.path.exists(os.path.join(output_directory, f"{base_name}_{counter}.jpg")):
                counter += 1
            output_image_path = os.path.join(output_directory, f"{base_name}_{counter}.jpg")

        convert_to_baseline_jpeg(input_image_path, output_image_path)
