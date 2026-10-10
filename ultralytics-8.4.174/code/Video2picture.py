import os
import cv2

# ========== 只需要修改这里 ==========
VIDEO_PATH = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/VideosCapture/scut.mp4"   # 给定的视频文件路径
OUTPUT_DIR = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/Make_dataset/scut/images"            # 输出根目录，会自动创建
INTERVAL = 5                   # 每隔多少帧取一张
IMG_EXT = ".jpg"                 # 图片格式：.jpg 或 .png
JPG_QUALITY = 95                 # JPG 质量 0-100
# ===================================

def imwrite_unicode(path, img, params=None):
    """支持中文/特殊字符路径的图片写入"""
    ext = os.path.splitext(path)[1]
    ok, buf = cv2.imencode(ext, img, params if params else [])
    if ok:
        buf.tofile(path)
    return ok


def extract_frames(video_path, output_dir, interval=10,
                   img_ext=".jpg", jpg_quality=95):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"无法打开视频: {video_path}")

    os.makedirs(output_dir, exist_ok=True)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    duration = total_frames / fps if fps > 0 else 0

    # 获取视频文件名（不带扩展名）
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    print(f"[视频] {video_path}")
    print(f"[信息] 总帧数: {total_frames} | FPS: {fps:.2f} | 时长: {duration:.2f}s")
    print(f"[输出] {output_dir}  (每 {interval} 帧取一张)")

    frame_idx = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % interval == 0:
            filename = f"{video_name}_{frame_idx:08d}{img_ext}"
            filepath = os.path.join(output_dir, filename)

            if img_ext.lower() in (".jpg", ".jpeg"):
                imwrite_unicode(filepath, frame,
                                [cv2.IMWRITE_JPEG_QUALITY, jpg_quality])
            else:
                imwrite_unicode(filepath, frame)

            saved += 1
            if saved % 100 == 0:
                print(f"  已保存 {saved} 张 ...")

        frame_idx += 1

    cap.release()
    print(f"[完成] 共保存 {saved} 张图片\n")
    return saved


if __name__ == "__main__":
    # 用 os.path 获取视频名，并拼出输出子目录
    video_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]
    out_dir = os.path.join(OUTPUT_DIR, video_name)

    extract_frames(
        video_path=VIDEO_PATH,
        output_dir=out_dir,
        interval=INTERVAL,
        img_ext=IMG_EXT,
        jpg_quality=JPG_QUALITY
    )