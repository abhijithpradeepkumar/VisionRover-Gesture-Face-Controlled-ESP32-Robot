import cv2
import time

STREAM_URL = "http://192.168.1.6:81/stream"

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Cannot open camera.")
    exit()

prev = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    fps = 1/(time.time()-prev)
    prev = time.time()

    h,w,_ = frame.shape

    cx = w//2
    cy = h//2

    # Crosshair
    cv2.line(frame,(cx-20,cy),(cx+20,cy),(0,255,0),2)
    cv2.line(frame,(cx,cy-20),(cx,cy+20),(0,255,0),2)

    cv2.putText(frame,
                f"FPS : {fps:.1f}",
                (20,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2)

    cv2.imshow("VisionRover Camera",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()