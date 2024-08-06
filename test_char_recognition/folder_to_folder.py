from ultralytics import YOLO
import cv2
import os
model = YOLO('best.pt')
import matplotlib.pyplot as plt

def plot_and_save_results(img_path, results,save_folder):
  #load img:
  img = cv2.imread(img_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  #loop thru results:
  for result in results:
    for box in result.boxes.data:
      x1, y1, x2, y2, conf, cls = box
      x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

      cv2.rectangle(img, (x1, y1), (x2,y2), (255, 0, 0), 2)

      label = f'{model.names[int(cls)]:{conf:.2f}}'
      #print(label)
      cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

  # Save the image
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    filename = os.path.basename(img_path)
    save_path = os.path.join(save_folder, filename)
    cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


#   plt.imshow(img)
#   plt.axis('off')
#   plt.show()




save_folder = r'C:\Users\ADMIN\Desktop\NumberPlate_dataset\ResultImages\part1 - (14)'
input_folder = r'C:\Users\ADMIN\Desktop\NumberPlate_dataset\Img_divided_part\part1 - (14)'

count = 0 
# Process all images in the input folder
for filename in os.listdir(input_folder):
    img_path = os.path.join(input_folder, filename)
    if os.path.isfile(img_path):
        results = model(img_path)
        plot_and_save_results(img_path, results, save_folder)

        count += 1
        print(count)
