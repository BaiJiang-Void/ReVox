import os
import subprocess
import soundfile as sf
import librosa


def preprocess_audio(input_path, output_path=None, target_sr=16000):
    """
    预处理音频：重采样到指定频率（默认16kHz）并转换为 wav 格式。

    Args:
        input_path (str): 输入音频/视频路径。
        output_path (str): 输出 wav 路径。
        target_sr (int): 目标采样率。
    """
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_std.wav"

    print(f"正在标准化音频: {input_path} -> {output_path} ({target_sr}Hz)")

    try:
        # 使用 librosa 加载并重采样
        data, sr = librosa.load(input_path, sr=target_sr)
        # 保存为 wav
        sf.write(output_path, data, target_sr)
        return output_path
    except Exception as e:
        print(f"音频重采样失败: {e}")
        # 如果 librosa 失败，尝试用 ffmpeg 作为备选方案
        return _preprocess_with_ffmpeg(input_path, output_path, target_sr)


def _preprocess_with_ffmpeg(input_path, output_path, target_sr):
    """备选方案：使用 FFmpeg 进行音频转换"""
    cmd = [
        'ffmpeg', '-i', input_path,
        '-ar', str(target_sr),
        '-ac', '1',  # 转为单声道
        '-y', output_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except Exception as e:
        print(f"FFmpeg 转换失败: {e}")
        return None


def get_audio_duration(file_path):
    """获取音频时长（秒）"""
    try:
        data, sr = sf.read(file_path)
        return len(data) / sr
    except:
        return 0