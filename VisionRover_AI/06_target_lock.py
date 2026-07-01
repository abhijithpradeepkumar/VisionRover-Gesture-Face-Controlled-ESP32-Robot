"""
=========================================================
VisionRover AI

Lesson 06 : Human Target Lock

New Concepts
------------
1. YOLO Object Tracking
2. Persistent IDs
3. Target Lock
4. Robot Memory

Goal
----
The first detected person becomes Human 1.
The robot ignores everyone else until Human 1 disappears.

=========================================================
"""

import cv2
from ultralytics import YOLO
import time

# ------------------------
# Load YOLO
# ------------------------

model = YOLO("yolov8n.pt")

STREAM_URL = "http://192.168.1.6:81/stream"

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Cannot connect to camera.")
    exit()

# ------------------------
# Robot Memory
# ------------------------

target_track_id = None
target_lost_time = None

LOST_TIMEOUT = 3  # seconds

# ------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    h, w = frame.shape[:2]
    frame_center = w // 2

    cv2.line(frame,
             (frame_center, 0),
             (frame_center, h),
             (0,255,255),
             2)

    # ------------------------
    # TRACK instead of DETECT
    # ------------------------

    results = model.track(
        frame,
        persist=True,
        verbose=False
    )

    current_target_found = False

    for result in results:

        if result.boxes.id is None:
            continue

        boxes = result.boxes

        for box, track_id in zip(boxes, boxes.id):

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            track_id = int(track_id)

            # Ignore non-humans

            if class_name != "person":

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

                continue

            # ------------------------
            # TARGET LOCK
            # ------------------------

            if target_track_id is None:

                target_track_id = track_id

            if track_id == target_track_id:

                current_target_found = True

                target_lost_time = None

                color = (0,255,0)

                label = "⭐ Human 1"

                status = "TARGET LOCKED"

            else:

                color = (0,165,255)

                label = "Human"

                status = ""

            # Draw

            cv2.rectangle(frame,
                          (x1,y1),
                          (x2,y2),
                          color,
                          3)

            cv2.putText(frame,
                        label,
                        (x1,y1-35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2)

            cv2.putText(frame,
                        status,
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

    # ------------------------
    # Lost Target
    # ------------------------

    if target_track_id is not None and not current_target_found:

        if target_lost_time is None:

            target_lost_time = time.time()

        elif time.time() - target_lost_time > LOST_TIMEOUT:

            target_track_id = None

            target_lost_time = None

    # ------------------------

    if target_track_id is None:

        cv2.putText(frame,
                    "Searching...",
                    (20,35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0,0,255),
                    2)

    else:

        cv2.putText(frame,
                    "STATUS : FOLLOWING HUMAN 1",
                    (20,35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)

    cv2.imshow("VisionRover AI", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()