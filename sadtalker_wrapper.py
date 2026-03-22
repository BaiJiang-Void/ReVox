import os
import subprocess
import sys
import shutil
import glob
from src.utils import audio_utils, image_utils, video_utils
from src.enhancers import denoise, superres


def run_sadtalker(source_image, driven_audio, output_path, sadtalker_path=None,
                  enhancer=None, denoise_flag=False, superres_flag=False, superres_scale=2,
                  extract_info=False, info_json=None,
                  sadtalker_python=None, size=256, **kwargs):
    if not sadtalker_python:
        sadtalker_python = sys.executable
    if not sadtalker_path:
        src_path = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(src_path)
        sadtalker_path = os.path.join(os.path.dirname(project_root), 'SadTalker')
    if not os.path.exists(sadtalker_path):
        raise FileNotFoundError(f"未找到 SadTalker 目录: {sadtalker_path}")
    temp_dir = os.path.abspath(os.path.join(os.getcwd(), 'temp_revox'))
    os.makedirs(temp_dir, exist_ok=True)
    try:
        # 1. 预处理
        print("正在预处理输入数据...")
        std_image = os.path.join(temp_dir, "temp_img.png")
        image_utils.resize_and_pad(source_image, std_image)
        std_audio = os.path.join(temp_dir, "temp_audio.wav")
        audio_utils.preprocess_audio(driven_audio, std_audio)
        if denoise_flag:
            print("正在执行音频降噪...")
            denoised_audio = os.path.join(temp_dir, "temp_audio_denoised.wav")
            denoise.process_audio(std_audio, denoised_audio)
            std_audio = denoised_audio
        # 2. 调用 SadTalker
        print(f"启动 SadTalker 推理进程 (Size: {size})...")
        env = os.environ.copy()
        env["PYTHONPATH"] = sadtalker_path + os.pathsep + env.get("PYTHONPATH", "")
        cmd = [
            sadtalker_python, 'inference.py',
            '--source_image', os.path.abspath(std_image),
            '--driven_audio', os.path.abspath(std_audio),
            '--result_dir', os.path.abspath(temp_dir),
            '--size', str(size)
        ]
        if kwargs.get('still'): cmd.append('--still')
        if enhancer: cmd.extend(['--enhancer', enhancer])
        subprocess.run(cmd, check=True, cwd=sadtalker_path, env=env)
        # 3. 寻找生成的视频
        generated_videos = glob.glob(os.path.join(temp_dir, '**/*.mp4'), recursive=True)
        if not generated_videos:
            raise RuntimeError("SadTalker 生成视频失败")
        raw_video = max(generated_videos, key=os.path.getmtime)
        # 4. 后处理增强
        video_to_merge = raw_video
        if superres_flag:
            print(f"正在执行视频超分 ({superres_scale}x)...")
            upscaled_video = os.path.join(temp_dir, "temp_upscaled.mp4")
            superres.enhance_video(raw_video, upscaled_video, scale=superres_scale)
            video_to_merge = upscaled_video
        # 5. 合并音视频
        print("正在合成最终视频并清理...")
        video_utils.merge_audio_video(video_to_merge, std_audio, output_path)
        if extract_info:
            info = video_utils.extract_video_info(output_path, save_json=info_json)
            print(f"处理完成! 最终分辨率: {info['width']}x{info['height']}")
        return output_path
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    print(f"项目根目录: {project_root}")
    # 调用测试
    run_sadtalker(
        source_image=os.path.join(project_root, "examples", "image_test.png"),
        driven_audio=os.path.join(project_root, "examples", "audio_test.wav"),
        output_path=os.path.join(project_root, "examples", "test_output_final.mp4"),
        enhancer=None,
        still=True,
        denoise_flag=True,
        superres_flag=True,
        superres_scale=2,
        extract_info=True,
        info_json=os.path.join(project_root, "examples", "test_info.json")
    )