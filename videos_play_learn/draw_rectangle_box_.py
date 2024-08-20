import cv2
import os

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
    return {'orig_x1':orig_x1,'orig_y1':orig_y1,'orig_x2':orig_x2, 'orig_y2':orig_x2}

# Path to your video file
video_path = r"C:\Users\ADMIN\Desktop\PAVAN\recodeing\sample.mp4"
selectd_data = selected_coordinates(video_path)
print(selectd_data)
