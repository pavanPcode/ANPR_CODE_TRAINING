from ultralytics import YOLO

character_model = YOLO('best_char_1630.pt')

from ultralytics import YOLO

character_model = YOLO('best_char_1630.pt')

def single_line_char_detect(number_plate_img):
    # Detect characters
    char_results = character_model(number_plate_img)
    # Extract, sort, and filter boxes in one step
    unique_boxes = {}
    for result in char_results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box[:6]  # Unpack the values correctly
            coord_key = (int(x1), int(y1), int(x2), int(y2))  # Convert coordinates to integers
            if coord_key not in unique_boxes or conf > unique_boxes[coord_key][4]:
                unique_boxes[coord_key] = (int(x1), int(y1), int(x2), int(y2), conf, int(cls))

    # Initialize an empty string to store the plate text
    plate_text = ""
    # Sort the unique boxes by x1 (left-to-right)
    sorted_boxes = sorted(unique_boxes.values(), key=lambda b: b[0])
    # Loop through the sorted boxes and construct the plate text
    for x1, y1, x2, y2, conf, cls in sorted_boxes:
        plate_text += character_model.names[cls]
    print(f"Vehicle number plate: {plate_text}")

number_plate_img = "88.jpeg"
single_line_char_detect(number_plate_img)
