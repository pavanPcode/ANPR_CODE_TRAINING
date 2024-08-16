from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load the YOLO model
model = YOLO('best_char_1630.pt')

# Image path
img_path = r"img.png"

# Run inference
results = model(img_path)

def plot_results(img_path, results):
    # Load image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # List to store boxes for sorting
    boxes_list = []

    # Extract boxes and add to list
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            boxes_list.append((int(x1), int(y1), int(x2), int(y2), conf, cls))

    # Sort boxes primarily by y1 (top-to-bottom) and secondarily by x1 (left-to-right)
    boxes_list.sort(key=lambda b: (b[1], b[0]))

    # Determine the line separation threshold
    y_coords = [box[1] for box in boxes_list]
    median_y = sorted(y_coords)[len(y_coords) // 2]

    # Separate the boxes into two lines
    line1 = [box for box in boxes_list if box[1] < median_y]
    line2 = [box for box in boxes_list if box[1] >= median_y]

    # Sort characters in each line by x1 (left-to-right)
    line1.sort(key=lambda b: b[0])
    line2.sort(key=lambda b: b[0])

    # Concatenate labels from each line
    plate_text_line1 = ""
    plate_text_line2 = ""

    for x1, y1, x2, y2, conf, cls in line1:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        label = f'{model.names[int(cls)]:{conf:.2f}}'
        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
        print(f'{label} - Coordinates: {coordinates}')
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        plate_text_line1 += label

    for x1, y1, x2, y2, conf, cls in line2:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        label = f'{model.names[int(cls)]:{conf:.2f}}'
        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
        print(f'{label} - Coordinates: {coordinates}')
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        plate_text_line2 += label

    # Concatenate text from both lines
    final_plate_text = plate_text_line1 + plate_text_line2
    print(f"vehicle_numberplate : {final_plate_text}")

    # Show the image with bounding boxes and labels
    plt.imshow(img)
    plt.axis('off')
    plt.show()

plot_results(img_path, results)
