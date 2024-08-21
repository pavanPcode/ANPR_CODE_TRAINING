import cv2
from ultralytics import YOLO
import os
import time
from datetime import datetime

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
video_path = r"C:\Users\ADMIN\Desktop\PAVAN\recodeing\cars.mp4"

# Initialize the video stream (0 for default webcam, or use the video file path)
video_stream = cv2.VideoCapture(video_path)

# Folder where you want to save the output images
output_folder = 'path_to_your_output_folder'
os.makedirs(output_folder, exist_ok=True)

# Set the desired frames per second (FPS) rate
desired_fps = 1  # Adjust this value to process more or fewer frames per second

# Get the original frames per second (FPS) of the video
original_fps = video_stream.get(cv2.CAP_PROP_FPS)
frames_to_skip = int(original_fps // desired_fps)

frame_count = 0
start_time = time.time()

# Set the desired window size
window_name = 'YOLOv8 Vehicle Detection'
window_width = 800
window_height = 600

# Create a named window and set its size
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, window_width, window_height)

while True:
    ret, frame = video_stream.read()

    if not ret:
        break

    # Skip frames to achieve desired FPS
    if frame_count % frames_to_skip == 0:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Extract the predictions
        predictions = results[0]

        # Draw the detected objects on the frame
        for box in predictions.boxes.xyxy.cpu().numpy():  # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box[:4])  # Convert coordinates to integers
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Get the current time with seconds
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Display the current time on the frame
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Save the detected frame to the output folder
        output_image_path = os.path.join(output_folder, f'detected_frame_{frame_count}.jpg')
        cv2.imwrite(output_image_path, frame)

        # Display the frame with detections and the current time
        cv2.imshow(window_name, frame)

    frame_count += 1

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('end', datetime.now())

# Release the video stream and close windows
video_stream.release()
cv2.destroyAllWindows()

print(f"Detection complete. Frames saved in: {output_folder}")
