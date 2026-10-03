import cv2
import numpy as np
# from ultralytics import YOLO

# Initialize models globally so they load only once when the server starts
# yolo_model = YOLO('yolov8_vehicle_weights.pt')

def process_image(image_bytes: bytes) -> tuple[str, str]:
    """
    Takes raw image bytes, runs YOLOv8 for vehicle type and OCR for the plate.
    """
    # Convert incoming bytes to an OpenCV image array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # TODO: Pass 'img' into your YOLO model
    # results = yolo_model(img)
    # Extract bounding boxes, crop plate, run OCR...

    # Simulated output for testing the API logic
    detected_type = "Car"
    plate_number = "WP CAA-1234"
    
    return detected_type, plate_number