import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

STREAM_URL = "http://192.168.1.6:81/stream"

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Cannot connect to camera")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    results = model(frame, verbose=False)

    human_count = 0

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            if class_name == "person":

                human_count += 1

                color = (0,255,0)

                label = "Human Detected"

            else:

                color = (255,0,0)

                label = class_name

            cv2.rectangle(frame,
                          (x1,y1),
                          (x2,y2),
                          color,
                          2)

            cv2.putText(frame,
                        f"{label} {confidence:.2f}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

    cv2.putText(frame,
                f"Humans Detected : {human_count}",
                (20,35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.imshow("VisionRover AI", frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()