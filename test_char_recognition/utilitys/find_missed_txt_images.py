import os

def check_images_for_txt_files(folder_path):
    # Get list of all files in the folder
    files_in_folder = os.listdir(folder_path)
    
    # Filter out jpg and png files
    image_files = [file for file in files_in_folder if file.lower().endswith(('.jpg', '.png'))]
    
    for image_file in image_files:
        # Construct the corresponding txt file name
        txt_file = os.path.splitext(image_file)[0] + '.txt'
        # Check if the txt file exists in the folder
        if txt_file not in files_in_folder:
            print(f"Text file for image '{image_file}' does not exist.")

# Specify the path to your folder
folder_path = r'C:\Users\ADMIN\Desktop\NumberPlate_dataset\Img_divided_part\part1 -pavan - FINAL'

# Call the function
check_images_for_txt_files(folder_path)
