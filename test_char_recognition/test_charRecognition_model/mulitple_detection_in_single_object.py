from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO('best_char_1630.pt')

#img_path = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\test_char_recognition\NumberPlatesForTesting\1\part1-input\000000144.jpg"
img_path = r"number_plate_729_460.jpg"
results = model(img_path)

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

    # Sort boxes by y1 (top-to-bottom) and then by x1 (left-to-right)
    boxes_list.sort(key=lambda b: ( b[0]))
    # Sort boxes by y1 (top-to-bottom) and then by x1 (left-to-right)
    #boxes_list.sort(key=lambda b: (b[1], b[0]))


    # Print sorted boxes and their x1 coordinates
    print("Sorted bounding boxes with x1 coordinates:")
    for box in boxes_list:
        print(box, box[0])
    plate_text = ""
    # Loop through sorted boxes and draw them
    for x1, y1, x2, y2, conf, cls in boxes_list:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        label = f'{model.names[int(cls)]}:{conf:.2f}'
        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
        print(f'{label} - Coordinates: {coordinates}')
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        plate_text  += label
    print(f"vehicle_numberplate : {plate_text}")

    plt.imshow(img)
    plt.axis('off')
    plt.show()

plot_results(img_path, results)
