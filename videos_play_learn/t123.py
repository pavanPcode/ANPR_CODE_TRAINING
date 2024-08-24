import cv2 as cv

video_path = r"C:\Users\ADMIN\Desktop\PAVAN\recodeing\sample.mp4"
# Open the video file
video = cv.VideoCapture(video_path)

# Check if the video file opened successfully
if not video.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video dimensions
frame_width = int(video.get(3))  # Width of the frames in the video
frame_height = int(video.get(4)) # Height of the frames in the video
size = (frame_width, frame_height) # Tuple with (width, height)
print(f"Video dimensions: {size}")

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('./outputs/uk_dash_2.avi', fourcc, 20.0, size)

# Loop to read and display frames
while True:
    ret, frame = video.read()  # Read a frame from the video

    # If the frame was not retrieved successfully, break the loop
    if not ret:
        print("End of video or error reading the frame.")
        break

    # Write the frame to the output video file
    out.write(frame)

    # Display the frame in a window
    cv.imshow('Video Playback', frame)

    # Wait for 25ms and check if the 'q' key is pressed to exit the loop
    if cv.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects, and close all OpenCV windows
video.release()
out.release()
cv.destroyAllWindows()
