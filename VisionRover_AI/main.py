import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

STREAM_URL = "http://192.168.1.6:81/stream"

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Cannot connect to ESP32-CAM")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    # AI Inference
    results = model(frame, verbose=False)

    annotated_frame = results[0].plot()

    cv2.imshow("VisionRover AI", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()