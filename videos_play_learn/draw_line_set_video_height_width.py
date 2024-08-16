import cv2
import datetime
import time

# Path to your video file
video_path = r"C:\Users\ADMIN\Desktop\PAVAN\recodeing\sample.mp4"

print('start', datetime.datetime.now())

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the video's frame rate
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps, 'fps')
frame_duration = 1 / fps  # Duration of each frame in seconds

# Read and display the video frames
start_time = time.time()
frame_count = 0

# Define the desired window size (you can adjust these values)
screen_width = 1080  # Desired width of the video window
screen_height = 680  # Desired height of the video window

while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the video

    if not ret:
        break  # Exit the loop when the video ends

    # Resize the frame to fit the screen
    resized_frame = cv2.resize(frame, (screen_width, screen_height))

    # Display the frame
    cv2.imshow('Video', resized_frame)

    # Calculate the time to wait until the next frame
    frame_count += 1
    elapsed_time = time.time() - start_time
    expected_time = frame_count * frame_duration
    # Adjust the sleep time to sync with the video's FPS
    if expected_time > elapsed_time:
        time.sleep(expected_time - elapsed_time)

    # Press 'q' to exit the video early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('end', datetime.datetime.now())

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
