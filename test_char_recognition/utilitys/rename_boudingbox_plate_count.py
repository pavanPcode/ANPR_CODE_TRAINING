import os
import shutil

data = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
    7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N',
    14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U',
    21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: '0', 27: '1',
    28: '2', 29: '3', 30: '4', 31: '5', 32: '6', 33: '7', 34: '8', 35: '9'
}

char_count = {}

def rename_files_in_directory(directory_path, new_dir):
    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a valid directory.")
        return

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    img_count = 0

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        base_name, ext = os.path.splitext(filename)

        if ext == '.txt':
            try:
                with open(file_path, 'r') as fileread:
                    cordinates = fileread.readlines()
                    numberplate = ""
                    for character in cordinates:
                        num = int(character.split()[0])
                        word = data[num]
                        numberplate += word

                        if word in char_count:
                            char_count[word] += 1
                        else:
                            char_count[word] = 1

                    new_filename = f'{base_name}_{numberplate}{ext}'
                    new_file_path = os.path.join(new_dir, new_filename)
                    shutil.copy(file_path, new_file_path)

                    old_img_name_png = f'{base_name}.png'
                    old_img_name_jpg = f'{base_name}.jpg'
                    old_img_path_png = os.path.join(directory_path, old_img_name_png)
                    old_img_path_jpg = os.path.join(directory_path, old_img_name_jpg)

                    if os.path.exists(old_img_path_png):
                        new_img_filename = f'{base_name}_{numberplate}.png'
                        shutil.copy(old_img_path_png, os.path.join(new_dir, new_img_filename))
                    elif os.path.exists(old_img_path_jpg):
                        new_img_filename = f'{base_name}_{numberplate}.jpg'
                        shutil.copy(old_img_path_jpg, os.path.join(new_dir, new_img_filename))
                    else:
                        print("not exists : " ,old_img_path_png)

                    img_count += 1
                    print(img_count)

            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    print(char_count)

# Usage
directory = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\FINAL_images_without_plate_names"
new_dir = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\FINAL_images_with_plate_names"
rename_files_in_directory(directory, new_dir)
