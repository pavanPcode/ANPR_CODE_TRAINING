import cv2
import os

# Path to your video file
video_path = r"C:\Users\ADMIN\Desktop\PAVAN\recodeing\sample.mp4"
# or an RTSP stream
# video_path = 'rtsp://admin:P3r3nni@l@192.168.1.250:554/cam/realmonitor?channel=1&subtype=0'

# Global variables to store rectangle coordinates and control flow
drawing = False
ix, iy = -1, -1
x1, y1, x2, y2 = 0, 0, 0, 0
rectangle_drawn = False

# Directory to save the cropped images
output_dir = "cropped_images"
os.makedirs(output_dir, exist_ok=True)

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, x1, y1, x2, y2, rectangle_drawn

    if event == cv2.EVENT_LBUTTONDOWN and not rectangle_drawn:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        x1, y1, x2, y2 = ix, iy, x, y

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            x1, y1, x2, y2 = ix, iy, x, y
            rectangle_drawn = True  # Fix the rectangle so it can't be edited
            print(f"Rectangle coordinates fixed: ({x1}, {y1}), ({x2}, {y2})")
            return x1, y1, x2, y2

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Error: Could not read the video frame.")
    cap.release()
    exit()

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
    if rectangle_drawn:
        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Video', frame_copy)

    # Press 's' to save the cropped image after drawing the rectangle
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and rectangle_drawn:
        # Calculate the original rectangle coordinates before resizing
        orig_x1 = int(x1 * (frame.shape[1] / screen_width))
        orig_y1 = int(y1 * (frame.shape[0] / screen_height))
        orig_x2 = int(x2 * (frame.shape[1] / screen_width))
        orig_y2 = int(y2 * (frame.shape[0] / screen_height))

        # Crop the selected region from the original frame
        cropped_image = frame[orig_y1:orig_y2, orig_x1:orig_x2]

        # Save the cropped image
        save_path = os.path.join(output_dir, "cropped_image.png")
        cv2.imwrite(save_path, cropped_image)
        print(f"Cropped image saved at {save_path}")
        break
    elif key == ord('q'):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
