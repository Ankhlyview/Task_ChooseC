from ultralytics import YOLO

model  = YOLO(r"/home/adh-a-a/ultralytics/runs/detect/train-2/weights/best.pt")
model.predict(
    source = 1,
    save = False,
    show = True,
)
## 可以预测图片，文件夹，视频，摄像头，一些网址
## https://docs.ultralytics.com/modes/predict
## vistualize竟然可以看到特征图()