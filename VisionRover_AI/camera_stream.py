import cv2

CAMERA_URL = "http://192.168.1.6:81/stream"

cap = cv2.VideoCapture(CAMERA_URL)

if not cap.isOpened():
    print("Cannot connect to camera")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("VisionRover Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()