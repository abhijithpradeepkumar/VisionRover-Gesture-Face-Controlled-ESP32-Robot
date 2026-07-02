import cv2
from ultralytics import YOLO

# ------------------------
# Load YOLO
# ------------------------

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

    h, w = frame.shape[:2]
    frame_center = w // 2

    # Draw image center
    cv2.line(frame,
             (frame_center, 0),
             (frame_center, h),
             (0,255,255),
             2)

    # Faster inference
    results = model(
        frame,
        imgsz=320,
        verbose=False
    )

    # --------------------------------
    # Find biggest person
    # --------------------------------

    biggest_person = None
    biggest_area = 0

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            if model.names[cls] != "person":
                continue

            x1,y1,x2,y2 = map(int,box.xyxy[0])

            area = (x2-x1)*(y2-y1)

            if area > biggest_area:

                biggest_area = area
                biggest_person = (x1,y1,x2,y2)

    robot_command = "SEARCHING"

    # --------------------------------
    # Draw ALL detections
    # --------------------------------

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])
            name = model.names[cls]

            conf = float(box.conf[0])

            x1,y1,x2,y2 = map(int,box.xyxy[0])

            # ----------------------------
            # PERSON
            # ----------------------------

            if name == "person":

                if biggest_person is not None and (x1,y1,x2,y2) == biggest_person:

                    color=(0,255,0)

                    label="TARGET HUMAN"

                    center_x=(x1+x2)//2

                    width=x2-x1

                    # Robot decision

                    if width>220:

                        robot_command="STOP"

                    elif center_x < frame_center-60:

                        robot_command="TURN LEFT"

                    elif center_x > frame_center+60:

                        robot_command="TURN RIGHT"

                    else:

                        robot_command="FORWARD"

                else:

                    color=(0,165,255)

                    label="Human"

            else:

                color=(255,0,0)

                label=name

            cv2.rectangle(frame,
                          (x1,y1),
                          (x2,y2),
                          color,
                          2)

            cv2.putText(frame,
                        label,
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

    # Dashboard

    cv2.rectangle(frame,
                  (0,0),
                  (w,55),
                  (40,40,40),
                  -1)

    cv2.putText(frame,
                f"COMMAND : {robot_command}",
                (20,35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.imshow("VisionRover AI",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()