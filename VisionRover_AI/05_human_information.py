import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

STREAM_URL = "http://192.168.1.6:81/stream"

cap = cv2.VideoCapture(STREAM_URL)

FRAME_CENTER_COLOR = (0, 255, 255)

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    h, w, _ = frame.shape

    frame_center = w // 2

    # Draw frame center line
    cv2.line(frame,
             (frame_center, 0),
             (frame_center, h),
             FRAME_CENTER_COLOR,
             2)

    results = model(frame, verbose=False)

    human_count = 0

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            if class_name == "person":

                human_count += 1

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                width = x2 - x1
                height = y2 - y1

                if width < 80:
                    distance = "Far"
                elif width < 180:
                    distance = "Medium"
                else:
                    distance = "Near"

                if center_x < frame_center - 70:
                    direction = "LEFT"

                elif center_x > frame_center + 70:
                    direction = "RIGHT"

                else:
                    direction = "CENTER"

                cv2.rectangle(frame,
                              (x1, y1),
                              (x2, y2),
                              (0,255,0),
                              2)

                cv2.circle(frame,
                           (center_x, center_y),
                           5,
                           (0,0,255),
                           -1)

                cv2.putText(frame,
                            "Human Detected",
                            (x1, y1-40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0,255,0),
                            2)

                cv2.putText(frame,
                            f"{distance} | {direction}",
                            (x1, y1-15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0,255,255),
                            2)

            else:

                cv2.rectangle(frame,
                              (x1,y1),
                              (x2,y2),
                              (255,0,0),
                              2)

                cv2.putText(frame,
                            class_name,
                            (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (255,0,0),
                            2)

    cv2.putText(frame,
                f"Humans : {human_count}",
                (20,35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.imshow("VisionRover AI", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()