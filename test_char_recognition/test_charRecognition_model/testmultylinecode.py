from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np
# Load the YOLO model
model = YOLO('best_char_1630.pt')



def plot_results(img_path, results):
    # Load image
    img = cv2.imread(img_path)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # List to store boxes for sorting
    #boxes_list = []
    img_height, img_width, _ = img.shape

    print(f"Image Height: {img_height} pixels")

    boxes_list = []
    # Extract boxes and add to list
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box[:6]
            boxes_list.append((int(x1), int(y1), int(x2), int(y2), conf, int(cls)))
            coord_key = (int(x1), int(y1), int(x2), int(y2))

    # Sort boxes primarily by y1 (top-to-bottom) and secondarily by x1 (left-to-right)
    boxes_list.sort(key=lambda b: (b[1], b[0]))

    # Improved separation and sorting
    # Separate boxes into lines based on y-coordina

    lines = []
    current_line = []
    last_y = -1  # Start with an invalid last_y value
    if img_height > 0 and img_height <= 60:
        y_threshold = 0
    elif img_height > 60 and img_height <= 250:
        y_threshold = 10
    elif img_height > 250 and img_height <  500:
        y_threshold = 30
    else: 
        y_threshold = 50
    print(f"{img_height} pixels")
    print(y_threshold)
    # Iterate over boxes to separate them into lines based on y1
    for box in boxes_list:
        x1, y1, x2, y2, conf, cls, = box[:6]
        #print("y_threshold:", y_threshold)
        if last_y == 1 or abs(y1 - last_y) < y_threshold:  # Use height to distinguish lines
            current_line.append(box)
        else:
            # If a new line is detected, sort the current line by x1 and store it
            lines.append(sorted(current_line, key=lambda b: b[0]))
            current_line = [box]  # Start a new line with the current box
        
        last_y = y1  # Update last_y to the current box's y1

    # Append the last line
    if current_line:
        lines.append(sorted(current_line, key=lambda b: b[0]))

    # Format the final plate text
    final_plate_text = ""
    for line in lines:
        previous_coords = None
        best_char = None
        best_conf = 0

        for x1, y1, x2, y2, conf, cls in line:
            char = model.names[int(cls)]
            current_coords = (x1, y1, x2, y2)

            # Check if the coordinates are the same or very close (within a small threshold)
            if previous_coords and abs(current_coords[0] - previous_coords[0]) < 10 and abs(
                    current_coords[2] - previous_coords[2]) < 5.5:
                if conf > best_conf:
                    best_char = char
                    best_conf = conf
            else:
                # Append the best character for the previous group of coordinates
                if best_char:
                    final_plate_text += best_char

                # Update to the current character and coordinates
                best_char = char
                best_conf = conf
                previous_coords = current_coords

            print(f"co ord : {current_coords}, Character: {char}, Confidence: {conf:.2f}")

        # Append the best character for the last group of coordinates
        if best_char:
            final_plate_text += best_char
        final_plate_text += " "  # Add a space between lines

    final_plate_text = final_plate_text.strip()
    print(f"Vehicle number plate: {final_plate_text}")

img_path = r"888.jpg"
# Run inference
results = model(img_path)
# Call the function to process and display the results
plot_results(img_path, results)
