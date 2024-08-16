import cv2
import os
from ultralytics import YOLO
from datetime import datetime
import random

# Load the YOLO model
number_plate_model = YOLO('customYOLO.pt')
character_model = YOLO('best_char_1630.pt')

def extract_frames(video_path, output_folder, frame_interval=30):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
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

        # Save every `frame_interval`-th frame
        if frame_count % frame_interval == 0:
            # frame_filename = os.path.join(output_folder, f"frame_{extracted_count:04d}.jpg")
            # cv2.imwrite(frame_filename, frame)
            # extracted_count += 1

            # Detect number plates
            print(datetime.now())
            number_plate_results = number_plate_model(frame)
            print(datetime.now(),extracted_count)
            for result in number_plate_results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # Draw the bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    label = f'{number_plate_model.names[int(cls)]}: {conf:.2f}'
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    # Extract the number plate image from the frame
                    number_plate_img = frame[y1:y2, x1:x2]

                    #detect_char
                    char_results = character_model(number_plate_img)
                    img = cv2.cvtColor(number_plate_img, cv2.COLOR_BGR2RGB)
                    # List to store boxes for sorting
                    boxes_list = []
                    # Loop through results
                    for result in char_results:
                        for box in result.boxes.data:
                            x1, y1, x2, y2, conf, cls = box
                            boxes_list.append((int(x1), int(y1), int(x2), int(y2), conf, cls))
                    # Sort boxes by x1 (left-to-right)
                    boxes_list.sort(key=lambda b: b[0])
                    plate_text = ""
                    # Loop through sorted boxes and draw them
                    for x1, y1, x2, y2, conf, cls in boxes_list:
                        label = f'{character_model.names[int(cls)]}'
                        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
                        # print(f'{label} - Coordinates: {coordinates}')
                        plate_text += label
                    print(f"Vehicle number plate: {plate_text}")
                    #return plate_text
                    # Save the number plate image
                    random_int = random.randint(100, 1000)
                    number_plate_img_path = os.path.join(output_folder,
                                                         f"number_plate_{plate_text}_{random_int}.jpg")
                    cv2.imwrite(number_plate_img_path, number_plate_img)

                    #save vehicle image
                    frame_filename = os.path.join(output_folder, f"frame_{extracted_count:04d}.jpg")
                    cv2.imwrite(frame_filename, frame)

                    extracted_count += 1



        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Extracted {extracted_count} frames from the video.")


# Usage
video_path = r"license_plate.mp4"
output_folder = "numberplates_images"
frame_interval = 60  # Change this to save a different number of frames per second

extract_frames(video_path, output_folder, frame_interval)
