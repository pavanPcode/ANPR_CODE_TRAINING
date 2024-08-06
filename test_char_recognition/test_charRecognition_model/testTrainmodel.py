from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO('best_char_1630.pt')

def plot_results(img_path, results):
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
      print(label)
      cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
  plt.imshow(img)
  plt.axis('off')
  plt.show()

img_path = r"C:\Users\ADMIN\Downloads\1.jpg"

results = model(img_path)
plot_results(img_path, results)