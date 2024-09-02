import os
from PIL import Image

def compress_images_in_folder(input_folder, output_folder, quality=30):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg")):  # Adjust for formats
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            img = Image.open(input_path)
            img.save(output_path, optimize=True, quality=quality)

            final_size = os.path.getsize(output_path) / 1024  # in KB
            print(f"Compressed {filename} to {final_size:.2f} KB")

input_folder = r"C:\Users\ADMIN\Desktop\vehicle_trained_dataset\images_parts\Indian Number Plates.v7i.yolov8\valid\images"
output_folder = r"C:\Users\ADMIN\Desktop\vehicle_trained_dataset\images_parts\Indian Number Plates.v7i.yolov8\valid"
compress_images_in_folder(input_folder, output_folder, quality=30)
