import cv2
import os
from ultralytics import YOLO
from datetime import datetime
import threading
import time
from PIL import Image as pilimg
from db_mysql import insert_vehicle_transaction
# Load the YOLO model
number_plate_model = YOLO('customYOLO.pt')
character_model = YOLO('best_char_1630.pt')

def char_detect(number_plate_img,frame,extracted_count):
    # Detect characters
    char_results = character_model(number_plate_img)
    # Load image
    img = frame
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # List to store boxes for sorting
    # boxes_list = []
    img_height, img_width, _ = img.shape

    print(f"Image Height: {img_height} pixels")

    boxes_list = []
    # Extract boxes and add to list
    for result in char_results:
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
    elif img_height > 250 and img_height < 500:
        y_threshold = 30
    else:
        y_threshold = 50
    print(f"{img_height} pixels")
    print(y_threshold)
    # Iterate over boxes to separate them into lines based on y1
    for box in boxes_list:
        x1, y1, x2, y2, conf, cls, = box[:6]
        # print("y_threshold:", y_threshold)
        if last_y == 1 or abs(y1 - last_y) < 10:  # Use height to distinguish lines
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
            char = character_model.names[int(cls)]
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

    # Save the number plate image
    number_plate_img_path = os.path.join(output_folder, f"NP_frame_{extracted_count:04d}_{final_plate_text}.jpg")
    cv2.imwrite(number_plate_img_path, number_plate_img)

    # save vehicle image
    frame_filename = os.path.join(output_folder, f"VI_frame_{extracted_count:04d}.jpg")
    cv2.imwrite(frame_filename, frame)
    ##
    # Resize the saved image using PIL
    max_size = (800, 800)
    with pilimg.open(frame_filename) as img:
        img.thumbnail(max_size)
        img.save(frame_filename)  # Overwrite the existing image with the resized version

    insert_vehicle_transaction(final_plate_text, frame_filename, number_plate_img_path)

def extract_frames(video_path, output_folder, selected_data,frame_interval=30):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    frame_count = 0
    extracted_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cropedframe = frame[selected_data['orig_y1']:selected_data['orig_y2'],
                selected_data['orig_x1']:selected_data['orig_x2']]
        cv2.imshow('Cropped Frame', cropedframe)

        # Resize the frame for display purposes
        screen_width = 1080
        screen_height = 680
        resized_frame = cv2.resize(frame, (screen_width, screen_height))

        # Save every `frame_interval`-th frame
        if frame_count % frame_interval == 0:
            # Detect number plates
            print(datetime.now())
            number_plate_results = number_plate_model(cropedframe,conf=0.3)
            c = 0
            for result in number_plate_results:
                print(c,'check')
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # Draw the bounding box and label on the frame
                    cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    label = f'{number_plate_model.names[int(cls)]}: {conf:.2f}'
                    cv2.putText(resized_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    # Extract the number plate image from the frame
                    number_plate_img = cropedframe[y1:y2, x1:x2]

                    extracted_count += 1
                    #char_detect(number_plate_img, frame, extracted_count)
                    # Create threads with arguments
                    thread1 = threading.Thread(target=char_detect, args=(number_plate_img, cropedframe, extracted_count))
                    # Start threads
                    thread1.start()
                    print(datetime.now(),extracted_count)
                    c = 1
                break

        # Get the current time with seconds
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Display the current time on the resized frame
        cv2.putText(resized_frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('Video', resized_frame)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Extracted {extracted_count} frames from the video.")


def selected_coordinates(video_path):
    # Variables to store rectangle coordinates and control flow
    drawing = [False]  # Use list to allow mutation inside nested function
    ix, iy = [-1], [-1]
    x1, y1, x2, y2 = [0], [0], [0], [0]
    rectangle_drawn = [False]

    # Directory to save the cropped images
    output_dir = "cropped_images"
    os.makedirs(output_dir, exist_ok=True)

    def draw_rectangle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and not rectangle_drawn[0]:
            drawing[0] = True
            ix[0], iy[0] = x, y

        elif event == cv2.EVENT_MOUSEMOVE and drawing[0]:
            x1[0], y1[0], x2[0], y2[0] = ix[0], iy[0], x, y

        elif event == cv2.EVENT_LBUTTONUP:
            if drawing[0]:
                drawing[0] = False
                x1[0], y1[0], x2[0], y2[0] = ix[0], iy[0], x, y
                rectangle_drawn[0] = True
                print(f"Rectangle coordinates fixed: ({x1[0]}, {y1[0]}), ({x2[0]}, {y2[0]})")

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None, None

    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read the video frame.")
        cap.release()
        return None, None

    # Resize the frame for display purposes
    screen_width = 1080
    screen_height = 680
    resized_frame = cv2.resize(frame, (screen_width, screen_height))

    # Create a window and set the mouse callback function
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', draw_rectangle)

    while True:
        # Display the frame with the rectangle (if it's being drawn)
        frame_copy = resized_frame.copy()
        if rectangle_drawn[0]:
            cv2.rectangle(frame_copy, (x1[0], y1[0]), (x2[0], y2[0]), (0, 255, 0), 2)

        cv2.imshow('Video', frame_copy)

        # Press 's' to save the cropped image after drawing the rectangle
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and rectangle_drawn[0]:
            # Calculate the original rectangle coordinates before resizing
            orig_x1 = int(x1[0] * (frame.shape[1] / screen_width))
            orig_y1 = int(y1[0] * (frame.shape[0] / screen_height))
            orig_x2 = int(x2[0] * (frame.shape[1] / screen_width))
            orig_y2 = int(y2[0] * (frame.shape[0] / screen_height))

            # Print coordinates for debugging
            print(f"Original rectangle coordinates: ({orig_x1}, {orig_y1}), ({orig_x2}, {orig_y2})")

            # Ensure coordinates are within the frame bounds and valid
            if (orig_x1 >= 0 and orig_y1 >= 0 and orig_x2 <= frame.shape[1] and orig_y2 <= frame.shape[0] and orig_x1 < orig_x2 and orig_y1 < orig_y2):
                # Crop the selected region from the original frame
                cropped_image = frame[orig_y1:orig_y2, orig_x1:orig_x2]

                # Check if cropped image is empty
                if cropped_image.size == 0:
                    print("Error: Cropped image is empty.")
                else:
                    # Save the cropped image
                    save_path = os.path.join(output_dir, "cropped_image.png")
                    cv2.imwrite(save_path, cropped_image)
                    print(f"Cropped image saved at {save_path}")
                break
            else:
                print("Error: Rectangle coordinates are out of frame bounds or invalid.")
        elif key == ord('q'):
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    return {'orig_x1':orig_x1,'orig_y1':orig_y1,'orig_x2':orig_x2, 'orig_y2':orig_y2}


# Usage
video_path = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\Anpr_Code\using_rtsp\license_plate.mp4"
#video_path = "rtsp://admin:P3r3nni@l@192.168.1.250:554/cam/realmonitor?channel=1&subtype=0"
output_folder = r"numberplates_images3"
frame_interval = 60  # Change this to save a different number of frames per second

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

selected_data = selected_coordinates(video_path)

extract_frames(video_path, output_folder,selected_data, frame_interval)
