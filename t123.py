from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load the models
number_plate_model = YOLO('customYOLO.pt')
character_model = YOLO('best_char_1630.pt')

def plot_results(img_path, results, model, color=(255, 0, 0)):
    # Load the image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Loop through results
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Draw rectangle around detected object
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Display label
            label = f'{model.names[int(cls)]}:{conf:.2f}'
            cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return img

# def detect_characters(number_plate_img):
#     results = character_model(number_plate_img)
#     return results


def detect_characters(number_plate_img):
    # Load image
    results = character_model(number_plate_img)
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # List to store boxes for sorting
    boxes_list = []

    # Loop through results
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            boxes_list.append((int(x1), int(y1), int(x2), int(y2), conf, cls))

    # Sort boxes by y1 (top-to-bottom) and then by x1 (left-to-right)
    boxes_list.sort(key=lambda b: ( b[0]))
    plate_text = ""
    # Loop through sorted boxes and draw them
    for x1, y1, x2, y2, conf, cls in boxes_list:
        label = f'{character_model.names[int(cls)]:{conf:.2f}}'
        coordinates = f'({x1}, {y1}), ({x2}, {y2})'
        print(f'{label} - Coordinates: {coordinates}')
        plate_text  += label
    print(f"vehicle_numberplate : {plate_text}")



def main(img_path):
    # Detect number plate
    number_plate_results = number_plate_model(img_path)

    # Plot number plate results
    img_with_number_plate = plot_results(img_path, number_plate_results, number_plate_model, color=(255, 0, 0))
    
    # Loop through the number plate results and extract the number plate image
    for result in number_plate_results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            number_plate_img = img_with_number_plate[y1:y2, x1:x2]
            # Detect characters in the number plate
            character_results = detect_characters(number_plate_img)

            # # Plot character results on number plate image
            # plot_results(number_plate_img, character_results, character_model, color=(0, 255, 0))
    
    plt.imshow(img_with_number_plate)
    plt.axis('off')
    plt.show()

img_path = r"C:\Users\ADMIN\Desktop\NumberPlate_dataset\Anpr_Code\NumberPlate_detection\only_vehicle_images\7_Afternoon_Images\VI_91727_2024-05-271305.jpg"

main(img_path)
