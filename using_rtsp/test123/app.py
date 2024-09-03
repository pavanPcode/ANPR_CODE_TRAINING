import cv2
import os
from ultralytics import YOLO
from datetime import datetime
import threading
import queue
from PIL import Image as pilimg
from db_sqllite import insert_vehicle_transaction

# Queue to store frames to be processed
frame_queue = queue.Queue()

# Load the YOLO models
number_plate_model = YOLO('customYOLO.pt')
character_model = YOLO('best_char_1630.pt')


def char_detect(number_plate_img, frame, extracted_count):
    # Detect characters
    char_results = character_model(number_plate_img)

    img_height, img_width, _ = frame.shape
    print(f"Image Height: {img_height} pixels")

    boxes_list = []
    for result in char_results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box[:6]
            boxes_list.append((int(x1), int(y1), int(x2), int(y2), conf, int(cls)))

    # Sort boxes primarily by y1 (top-to-bottom) and secondarily by x1 (left-to-right)
    boxes_list.sort(key=lambda b: (b[1], b[0]))

    lines = []
    current_line = []
    last_y = -1
    y_threshold = 50 if img_height >= 500 else (30 if img_height > 250 else (10 if img_height > 60 else 0))
    print(f"{img_height} pixels")
    print(f"Y threshold: {y_threshold}")

    for box in boxes_list:
        x1, y1, x2, y2, conf, cls = box
        if last_y == -1 or abs(y1 - last_y) < y_threshold:
            current_line.append(box)
        else:
            lines.append(sorted(current_line, key=lambda b: b[0]))
            current_line = [box]
        last_y = y1

    if current_line:
        lines.append(sorted(current_line, key=lambda b: b[0]))

    final_plate_text = ""
    for line in lines:
        previous_coords = None
        best_char = None
        best_conf = 0

        for x1, y1, x2, y2, conf, cls in line:
            char = character_model.names[int(cls)]
            current_coords = (x1, y1, x2, y2)

            if previous_coords and abs(current_coords[0] - previous_coords[0]) < 10 and abs(
                    current_coords[2] - previous_coords[2]) < 5.5:
                if conf > best_conf:
                    best_char = char
                    best_conf = conf
            else:
                if best_char:
                    final_plate_text += best_char
                best_char = char
                best_conf = conf
                previous_coords = current_coords

            print(f"Coords: {current_coords}, Character: {char}, Confidence: {conf:.2f}")

        if best_char:
            final_plate_text += best_char
        final_plate_text += " "

    final_plate_text = final_plate_text.strip()
    print(f"Vehicle number plate: {final_plate_text}")

    # Save the number plate image
    number_plate_img_path = os.path.join(output_folder, f"NP_frame_{extracted_count:04d}_{final_plate_text}.jpg")
    cv2.imwrite(number_plate_img_path, number_plate_img)

    # Save the vehicle image
    frame_filename = os.path.join(output_folder, f"VI_frame_{extracted_count:04d}.jpg")
    cv2.imwrite(frame_filename, frame)

    # Resize the saved image using PIL
    max_size = (800, 800)
    with pilimg.open(frame_filename) as img:
        img.thumbnail(max_size)
        img.save(frame_filename)

    insert_vehicle_transaction(final_plate_text, frame_filename, number_plate_img_path)


def extract_frames():
    extracted_count = 0
    while True:
        if not frame_queue.empty():
            cropedframe, resized_frame = frame_queue.get()

            # Debug print to check frame dimensions
            print(f"Cropedframe dimensions: {cropedframe.shape}")
            if cropedframe.shape[0] == 0 or cropedframe.shape[1] == 0:
                print("Error: Cropped frame has zero width or height.")
                continue

            # Detect number plates
            print("Processing frame")
            number_plate_results = number_plate_model(cropedframe, conf=0.3)
            for result in number_plate_results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Ensure valid cropping area
                    if x1 < x2 and y1 < y2:
                        number_plate_img = cropedframe[y1:y2, x1:x2]
                        extracted_count += 1
                        char_detect(number_plate_img, resized_frame, extracted_count)
                        print(datetime.now(), extracted_count)


def selected_coordinates(video_path, screen_width, screen_height):
    drawing = [False]
    ix, iy = [-1], [-1]
    x1, y1, x2, y2 = [0], [0], [0], [0]
    rectangle_drawn = [False]

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

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")

    if not cap.isOpened():
        print("Error: Could not open video.")
        return None, None

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read the video frame.")
        cap.release()
        return None, None

    resized_frame = cv2.resize(frame, (screen_width, screen_height))
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', draw_rectangle)

    orig_x1, orig_y1, orig_x2, orig_y2 = None, None, None, None

    while True:
        frame_copy = resized_frame.copy()
        if rectangle_drawn[0]:
            cv2.rectangle(frame_copy, (x1[0], y1[0]), (x2[0], y2[0]), (0, 255, 0), 2)

        cv2.imshow('Video', frame_copy)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and rectangle_drawn[0]:
            orig_x1 = int(x1[0] * (frame.shape[1] / screen_width))
            orig_y1 = int(y1[0] * (frame.shape[0] / screen_height))
            orig_x2 = int(x2[0] * (frame.shape[1] / screen_width))
            orig_y2 = int(y2[0] * (frame.shape[0] / screen_height))

            print(f"Original rectangle coordinates: ({orig_x1}, {orig_y1}), ({orig_x2}, {orig_y2})")

            if orig_x1 >= 0 and orig_y1 >= 0 and orig_x2 <= frame.shape[1] and orig_y2 <= frame.shape[
                0] and orig_x1 < orig_x2 and orig_y1 < orig_y2:
                cropped_image = frame[orig_y1:orig_y2, orig_x1:orig_x2]

                if cropped_image.size == 0:
                    print("Error: Cropped image is empty.")
                else:
                    save_path = os.path.join(output_dir, "cropped_image.png")
                    cv2.imwrite(save_path, cropped_image)
                    print(f"Cropped image saved at {save_path}")
                break
            else:
                print("Error: Rectangle coordinates are out of frame bounds or invalid.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return {'orig_x1': orig_x1, 'orig_y1': orig_y1, 'orig_x2': orig_x2, 'orig_y2': orig_y2}


# Main loop
if __name__ == "__main__":
    video_path = r"C:\Users\ADMIN\Downloads\recodeing\sample.mp4"
    output_folder = r"C:\Users\ADMIN\Desktop\Anpr_traning_pavan\Anpr_Code\using_rtsp\test123\numberplates_images3"
    frame_interval = 10

    screen_width = 640
    screen_height = 480

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get rectangle coordinates
    selected_data = selected_coordinates(video_path, screen_width, screen_height)

    if selected_data:
        # Start the YOLO inference thread
        yolo_thread = threading.Thread(target=extract_frames)
        yolo_thread.daemon = True
        yolo_thread.start()

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, (screen_width, screen_height))

            if selected_data:
                cropedframe = resized_frame[selected_data['orig_y1']:selected_data['orig_y2'],
                              selected_data['orig_x1']:selected_data['orig_x2']]

                # Debug print to check cropped frame dimensions
                print(f"Cropedframe dimensions: {cropedframe.shape}")

                if cropedframe.shape[0] > 0 and cropedframe.shape[1] > 0 and frame_count % frame_interval == 0:
                    # Put both the cropped and resized frame in the queue
                    frame_queue.put((cropedframe, resized_frame))

            # Optional: Display the resized frame for debugging
            cv2.imshow('Video', resized_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Error: Rectangle coordinates were not properly selected.")
