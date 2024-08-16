import cv2
import datetime
import time

# Path to your video file
video_path = r"C:\Users\ADMIN\Desktop\PAVAN\recodeing\sample.mp4"

# Global variables to store rectangle coordinates and control flow
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial coordinates
x1, y1, x2, y2 = 0, 0, 0, 0  # Rectangle coordinates
rectangle_drawn = False  # Flag to check if the rectangle is drawn
play_video = False  # Flag to control video playback

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, x1, y1, x2, y2, rectangle_drawn

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x1, y1, x2, y2 = ix, iy, x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1, x2, y2 = ix, iy, x, y
        rectangle_drawn = True
        print(f"Rectangle coordinates: ({x1}, {y1}), ({x2}, {y2})")

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

# Define the desired window size (you can adjust these values)
screen_width = 1080  # Desired width of the video window
screen_height = 680  # Desired height of the video window

# Create a named window and set the mouse callback function
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', draw_rectangle)

# Wait for the rectangle to be drawn
while not rectangle_drawn:
    ret, frame = cap.read()  # Read a frame from the video
    if not ret:
        break

    # Resize the frame to fit the screen
    resized_frame = cv2.resize(frame, (screen_width, screen_height))

    # Display the frame with the rectangle (if it's being drawn)
    if x1 != x2 and y1 != y2:
        cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Video', resized_frame)

    # Press 'p' to start playing the video after the rectangle is drawn
    if cv2.waitKey(1) & 0xFF == ord('p'):
        play_video = True
        break

# Start video playback after the rectangle is drawn and 'p' is pressed
if play_video:
    while cap.isOpened():
        ret, frame = cap.read()  # Read a frame from the video

        if not ret:
            break  # Exit the loop when the video ends

        # Resize the frame to fit the screen
        resized_frame = cv2.resize(frame, (screen_width, screen_height))

        # Draw the rectangle on the frame
        if x1 != x2 and y1 != y2:
            cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

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
