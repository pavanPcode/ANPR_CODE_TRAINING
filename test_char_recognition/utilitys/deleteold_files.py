import os
import time
from datetime import datetime, timedelta

def delete_old_files(folder_path, days_old):
    now = time.time()
    cutoff = now - (days_old * 86400)  # 86400 seconds in a day

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff:
                    print(f"Deleting {file_path}")
                    os.remove(file_path)

folder_path = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\Img_divided_part\part1 - (3)-pavan\test - Copy"
days_old = 10

delete_old_files(folder_path, days_old)
