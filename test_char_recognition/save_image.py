from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

model = YOLO('best (1).pt')

img_path = r"D:\PerennialCode\testTrain4_3.10\numberplates\00000054.jpg"

results = model(img_path)

print(results)


def plot_results(img_path, results):
    # Load img:
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Prepare a directory to save the cropped images
    base_dir = os.path.dirname(img_path)
    save_dir = os.path.join(base_dir, 'cropped_images')
    os.makedirs(save_dir, exist_ok=True)

    # Loop thru results:
    count = 0
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Crop the detected region
            cropped_img = img[y1:y2, x1:x2]

            # Save the cropped image with class name
            class_name = model.names[int(cls)]
            crop_filename = f'crop_{count}_{class_name}.jpg'
            crop_path = os.path.join(save_dir, crop_filename)
            cv2.imwrite(crop_path, cv2.cvtColor(cropped_img, cv2.COLOR_RGB2BGR))
            count += 1

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

            label = f'{class_name}:{conf:.2f}'
            print(label)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Save the annotated image
    output_path = os.path.splitext(img_path)[0] + '_annotated.jpg'
    cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    plt.imshow(img)
    plt.axis('off')
    plt.show()


plot_results(img_path, results)
