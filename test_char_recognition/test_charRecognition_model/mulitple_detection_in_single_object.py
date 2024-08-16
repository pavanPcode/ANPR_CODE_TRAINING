from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO('best_char_1630.pt')

# Load your image
img_path = r"img.png"
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
            boxes_list.append((int(x1), int(y1), int(x2), int(y2), float(conf), int(cls)))

    # Sort boxes by y1 (top-to-bottom) and then by x1 (left-to-right)
    boxes_list.sort(key=lambda b: (b[1], b[0]))

    # Dictionary to store the highest confidence boxes for unique coordinates
    unique_boxes = {}
    # Filter boxes to keep only the one with the highest confidence for each unique set of coordinates
    for box in boxes_list:
        x1, y1, x2, y2, conf, cls = box
        coord_key = (x1, y1, x2, y2)
        if coord_key not in unique_boxes or conf > unique_boxes[coord_key][4]:
            unique_boxes[coord_key] = box
    plate_text = ""

    # Loop through the filtered boxes and draw them
    for x1, y1, x2, y2, conf, cls in unique_boxes.values():
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        label = f'{model.names[cls]}:{conf:.2f}'
        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
        print(f'{label} - Coordinates: {coordinates}')
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        plate_text += model.names[cls]

    print(f"Vehicle number plate: {plate_text}")

    # Display the image with bounding boxes and labels
    plt.imshow(img)
    plt.axis('off')
    plt.show()


plot_results(img_path, results)
