import cv2
import os
import numpy as np


def resize_and_pad(image_path, output_path, target_size=(512, 512)):
    """
    将图片缩放并填充（Padding）到目标尺寸，保持原图比例。
    防止图片拉伸导致人脸畸形。
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"无法读取图片: {image_path}")

    h, w = img.shape[:2]
    scale = min(target_size[0] / w, target_size[1] / h)
    nw, nh = int(w * scale), int(h * scale)

    # 缩放图片
    img_resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_CUBIC)

    # 创建背景板 (中灰色填充，或者黑色)
    canvas = np.full((target_size[1], target_size[0], 3), 128, dtype=np.uint8)

    # 将缩放后的图片居中贴上去
    dx = (target_size[0] - nw) // 2
    dy = (target_size[1] - nh) // 2
    canvas[dy:dy + nh, dx:dx + nw] = img_resized

    cv2.imwrite(output_path, canvas)
    return output_path


def auto_crop_face(image_path, output_path):
    """
    利用 OpenCV 自带的 Haar 级联检测人脸并进行简单裁剪。
    (这是基础版，未来可以升级为 Dlib 或 MediaPipe)
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 加载预训练的人脸分类器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("未检测到人脸，将使用原图。")
        return resize_and_pad(image_path, output_path)

    # 选取最大的那张脸
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

    # 适当扩大裁剪范围（给头部留白）
    padding_w = int(w * 0.5)
    padding_h = int(h * 0.5)

    x1 = max(0, x - padding_w)
    y1 = max(0, y - padding_h)
    x2 = min(img.shape[1], x + w + padding_w)
    y2 = min(img.shape[0], y + h + padding_h)

    face_img = img[y1:y2, x1:x2]
    cv2.imwrite(output_path, face_img)

    # 最后再标准化一次尺寸
    return resize_and_pad(output_path, output_path)