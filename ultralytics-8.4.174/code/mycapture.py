import cv2
import os
from datetime import datetime

def record_video():
    """
    通过摄像头录制视频，支持开始/结束控制
    """
    # ========== 配置区域（可修改） ==========
    SAVE_DIR = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/VideosCapture"          # 视频保存目录（改成你想要的路径）
    CAMERA_INDEX = 2                 # 摄像头索引，0通常是默认摄像头
    FPS = 30.0                       # 帧率
    FRAME_WIDTH = 1280               # 画面宽度
    FRAME_HEIGHT = 720               # 画面高度
    # =======================================
    
    # 如果保存目录不存在，自动创建
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"已创建保存目录: {SAVE_DIR}")
    
    # 打开摄像头
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("错误：无法打开摄像头！")
        return
    
    # 设置摄像头参数
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    
    # 实际获取的分辨率
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    if actual_fps == 0:
        actual_fps = FPS
    
    print("=" * 50)
    print("摄像头录制程序已启动")
    print(f"分辨率: {actual_w} x {actual_h}")
    print(f"帧率: {actual_fps}")
    print(f"保存目录: {SAVE_DIR}")
    print("-" * 50)
    print("操作说明:")
    print("  按 's' 键 -> 开始录制")
    print("  按 'e' 键 -> 结束录制")
    print("  按 'q' 键 -> 退出程序")
    print("=" * 50)
    
    # 录制状态
    is_recording = False
    video_writer = None
    current_file = None
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("警告：读取摄像头帧失败")
            break
        
        # 如果正在录制，写入视频文件
        if is_recording:
            video_writer.write(frame)
            frame_count += 1
            
            # 在画面上显示录制状态
            cv2.circle(frame, (30, 30), 12, (0, 0, 255), -1)
            cv2.putText(frame, f"REC  {frame_count} frames",
                        (50, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)
        
        # 显示提示信息
        if is_recording:
            status_text = "Recording... Press 'e' to STOP"
            color = (0, 0, 255)
        else:
            status_text = "Ready. Press 's' to START"
            color = (0, 255, 0)
        
        cv2.putText(frame, status_text, (10, actual_h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # 显示画面
        cv2.imshow("Camera Recorder", frame)
        
        # 键盘控制
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s') and not is_recording:
            # ---- 开始录制 ----
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_file = os.path.join(SAVE_DIR, f"video_{timestamp}.mp4")
            
            # 使用 mp4v 编码器（兼容性好）
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                current_file, fourcc, actual_fps,
                (actual_w, actual_h)
            )
            
            if not video_writer.isOpened():
                print("错误：无法创建视频文件！")
                video_writer = None
                continue
            
            is_recording = True
            frame_count = 0
            print(f"▶ 开始录制: {current_file}")
        
        elif key == ord('e') and is_recording:
            # ---- 结束录制 ----
            is_recording = False
            if video_writer is not None:
                video_writer.release()
                video_writer = None
            
            print(f"■ 结束录制，共 {frame_count} 帧")
            print(f"  文件已保存: {current_file}")
        
        elif key == ord('q'):
            # ---- 退出程序 ----
            if is_recording:
                print("正在录制中，自动结束录制...")
                if video_writer is not None:
                    video_writer.release()
                    video_writer = None
                print(f"  文件已保存: {current_file}")
            print("退出程序")
            break
    
    # 释放资源
    cap.release()
    if video_writer is not None:
        video_writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    record_video()