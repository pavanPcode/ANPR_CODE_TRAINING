from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

model = YOLO('customYOLO.pt')

def plot_results(img_path, results):
  #load img:
  img = cv2.imread(img_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  #loop thru results:
  for result in results:
    for box in result.boxes.data:
      x1, y1, x2, y2, conf, cls = box
      print('box : ',x1, y1, x2, y2, conf, cls)
      x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

      cv2.rectangle(img, (x1, y1), (x2,y2), (255, 0, 0), 2)

      label = f'{model.names[int(cls)]:{conf:.2f}}'
      cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
  plt.imshow(img)
  plt.axis('off')
  plt.show()

img_path = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\Anpr_Code\NumberPlate_detection\only_vehicle_images\7_Afternoon_Images\VI_91727_2024-05-271305.jpg"

results = model(img_path)
plot_results(img_path, results)



# input_folder = r"only_vehicle_images\2_Evening_images_100"
# # Process all images in the input folder
# for filename in os.listdir(input_folder):
#     img_path = os.path.join(input_folder, filename)
#     if os.path.isfile(img_path):
#         results = model(img_path)
#         plate_text = plot_results(img_path, results)




