import os
import subprocess
import cv2
import json


def merge_audio_video(video_path, audio_path, output_path):
    """使用 FFmpeg 合并音视频轨道"""
    cmd = [
        'ffmpeg', '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-y', output_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 合并失败: {e.stderr.decode()}")
        return None


def get_video_specs(video_path):
    """快速获取视频的分辨率和帧率"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return {"width": width, "height": height, "fps": fps}


def convert_to_mp4(input_path, output_path):
    """将视频转换为标准的 H.264 mp4 格式（增强兼容性）"""
    cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-y', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def extract_video_info(video_path, save_json=None):
    """从原 video_info.py 迁移，提取视频元数据"""
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"无法打开视频: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    info = {
        "width": width,
        "height": height,
        "fps": round(fps, 2),
        "total_frames": total_frames,
        "duration": round(total_frames / fps, 2) if fps > 0 else 0,
        "file_size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2)
    }
    cap.release()

    if save_json:
        with open(save_json, 'w') as f:
            json.dump(info, f, indent=4)
    return info


def merge_audio_video(video_path, audio_path, output_path):
    """从 sadtalker_wrapper 迁移，统一音视频合并逻辑"""
    cmd = [
        'ffmpeg', '-i', video_path, '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
        '-map', '0:v:0', '-map', '1:a:0', '-y', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path