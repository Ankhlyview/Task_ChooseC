from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(2)
model = YOLO(r"/home/adh-a-a/ultralytics/runs/detect/train-2/weights/best.pt")


while True:
    ret, frame = cap.read()
    results = model(frame, conf=0.5, iou=0.5, line_width=2, show_labels=True)

    target = results[0].plot()

    cv2.imshow("Camera", target)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()