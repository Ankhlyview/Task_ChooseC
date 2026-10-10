import os
import shutil
import random

# ========== 只需要修改这里 ==========
IMG_DIR   = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/Make_dataset/scut/ori_images/scut"        # 图片文件夹
LABEL_DIR = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/Make_dataset/scut/ori_labels"        # 标签文件夹
OUT_DIR   = r"/home/adh-a-a/ultralytics/ultralytics-8.4.174/Make_dataset/scut/dataset"  # 输出数据集文件夹

VAL_RATIO = 0.2                      # 验证集比例（0.2 表示 20%）
SEED      = 42                       # 随机种子
CLASS_NAMES = None                   # 类别名称列表，如 ["cat", "dog"]
                                     # 如果为 None，则自动推断并命名为 class0, class1...
# ===================================


def create_yolo_dataset(img_dir, label_dir, out_dir,
                        val_ratio=0.2, class_names=None, seed=42):
    """将图片和标签整理成标准 YOLO 数据集。"""
    random.seed(seed)

    # 支持的图片扩展名
    img_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')

    # 1. 获取所有图片文件
    img_files = []
    for f in os.listdir(img_dir):
        ext = os.path.splitext(f)[1].lower()
        if ext in img_exts:
            img_files.append(f)

    if not img_files:
        print(f"在 {img_dir} 中没有找到图片文件！")
        return

    # 2. 检查标签是否存在，组成有效配对
    valid_pairs = []
    for img_file in img_files:
        base = os.path.splitext(img_file)[0]
        label_file = base + '.txt'
        label_path = os.path.join(label_dir, label_file)

        if os.path.isfile(label_path):
            valid_pairs.append((img_file, label_file))
        else:
            print(f"警告: 图片 {img_file} 缺少对应的标签 {label_file}，已跳过")

    if not valid_pairs:
        print("没有找到任何有效的图片-标签对！")
        return

    print(f"共找到 {len(valid_pairs)} 对有效的图片-标签。")

    # 3. 随机打乱并划分训练集/验证集
    random.shuffle(valid_pairs)
    val_count = int(len(valid_pairs) * val_ratio)
    val_pairs = valid_pairs[:val_count]
    train_pairs = valid_pairs[val_count:]

    # 4. 创建输出目录结构
    train_img_dir = os.path.join(out_dir, 'images', 'train')
    val_img_dir   = os.path.join(out_dir, 'images', 'val')
    train_lab_dir = os.path.join(out_dir, 'labels', 'train')
    val_lab_dir   = os.path.join(out_dir, 'labels', 'val')

    for d in (train_img_dir, val_img_dir, train_lab_dir, val_lab_dir):
        os.makedirs(d, exist_ok=True)

    # 5. 复制文件
    def copy_pairs(pairs, img_dst, lab_dst):
        for img_file, label_file in pairs:
            shutil.copy2(os.path.join(img_dir, img_file),
                         os.path.join(img_dst, img_file))
            shutil.copy2(os.path.join(label_dir, label_file),
                         os.path.join(lab_dst, label_file))

    copy_pairs(train_pairs, train_img_dir, train_lab_dir)
    copy_pairs(val_pairs,   val_img_dir,   val_lab_dir)

    print(f"训练集: {len(train_pairs)} 张图片")
    print(f"验证集: {len(val_pairs)} 张图片")

    # 6. 推断类别数或使用提供的类别名
    if class_names is None:
        max_class = -1
        for _, label_file in valid_pairs:
            with open(os.path.join(label_dir, label_file), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        cls_id = int(line.split()[0])
                        if cls_id > max_class:
                            max_class = cls_id
        nc = max_class + 1
        names = [f'class{i}' for i in range(nc)]
    else:
        names = class_names
        nc = len(names)

    # 7. 生成 data.yaml
    yaml_path = os.path.join(out_dir, 'data.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(f"path: {os.path.abspath(out_dir)}\n")
        f.write("train: images/train\n")
        f.write("val: images/val\n")
        f.write(f"nc: {nc}\n")
        f.write(f"names: {names}\n")

    print(f"\n数据集已生成到: {os.path.abspath(out_dir)}")
    print(f"data.yaml 已生成，类别数: {nc}，类别名称: {names}")


if __name__ == '__main__':
    create_yolo_dataset(
        img_dir=IMG_DIR,
        label_dir=LABEL_DIR,
        out_dir=OUT_DIR,
        val_ratio=VAL_RATIO,
        class_names=CLASS_NAMES,
        seed=SEED
    )