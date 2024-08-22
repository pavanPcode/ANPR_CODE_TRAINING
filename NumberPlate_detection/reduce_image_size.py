from PIL import Image

def resize_image(input_image_path, output_image_path, max_size):
    with Image.open(input_image_path) as img:
        img.thumbnail(max_size)  # No need to specify Image.ANTIALIAS
        img.save(output_image_path)

# Example usage
input_image_path = "44.jpg"
output_image_path = "123.jpg"
max_size = (800, 800)  # max width, max height

resize_image(input_image_path, output_image_path, max_size)
