from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/models/yolo11n.pt")
    model.train(data = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/ultralytics/cfg/datasets/ScutBadge.yaml",
                epochs=100,imgsz=640,batch=16,cache=False,workers=0,optimizer='Adam',)
    