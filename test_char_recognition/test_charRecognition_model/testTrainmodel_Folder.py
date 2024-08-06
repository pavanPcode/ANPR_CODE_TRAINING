from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os
import pandas as pd
import xlsxwriter  # Ensure this is imported

model = YOLO('best_char_1630.pt')

def plot_results(img_path, results):
    # Load image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # List to store boxes for sorting
    boxes_list = []

    # Loop through results
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            boxes_list.append((int(x1), int(y1), int(x2), int(y2), conf, cls))

    boxes_list.sort(key=lambda b: b[0])
    
    plate_text = ""
    # Loop through sorted boxes and draw them
    for x1, y1, x2, y2, conf, cls in boxes_list:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        label = f'{model.names[int(cls)]:{conf:.2f}}'
        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        plate_text += label
    
    print(f"vehicle_numberplate : {plate_text}")
    
    return plate_text

input_folder = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\test_char_recognition\NumberPlatesForTesting\Novotel_latest_anpr_imgs\3_03_08_2024\numberplate\7"

results_data = []

# Process all images in the input folder
for filename in os.listdir(input_folder):
    img_path = os.path.join(input_folder, filename)
    if os.path.isfile(img_path):
        results = model(img_path)
        plate_text = plot_results(img_path, results)

        results_data.append({'image_path': img_path, 'plate_text': plate_text})
        

# Save the results to an Excel file with hyperlinks
df = pd.DataFrame(results_data)
output_path = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\test_char_recognition\NumberPlatesForTesting\Novotel_latest_anpr_imgs\3_03_08_2024\numberplate\7.xlsx"

# Use the xlsxwriter engine to create hyperlinks
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add hyperlinks to the image paths
    for row_num, (image_path, plate_text) in enumerate(zip(df['image_path'], df['plate_text']), start=1):
        worksheet.write_url(row_num, 0, f'file:///{image_path}', string=image_path)

print(f"Results saved to {output_path}")
