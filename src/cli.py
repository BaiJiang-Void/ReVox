import sys
import os
import shutil
import time
import signal
import atexit
import argparse
import urllib.request
from pathlib import Path
from tqdm import tqdm
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from src.core.config_manager import ConfigManager
from src.core.logger import logger
from src.core.exceptions import ReVoxError
from src.utils.security_utils import (
    safe_path_check,
    validate_file_type,
    sanitize_filename,
    SecureFileOperations
)
from src.sadtalker_wrapper import run_sadtalker
from src.enhancers.superres import run_video_upscale
from src.utils.video_utils import merge_audio_video, check_ffmpeg_env
from src.utils.image_utils import resize_and_pad
from src.utils.info_utils import print_video_info


TEMP_FOLDERS = ["temp_revox", "temp_sadtalker"]
CLEANUP_TEMP = True
_cleaned = False

def cleanup_handler():
    global CLEANUP_TEMP, _cleaned
    if _cleaned:
        return
    if CLEANUP_TEMP:
        logger.info(">>> 正在执行工作空间深度清理...")
        for folder in TEMP_FOLDERS:
            if os.path.exists(folder):
                try:
                    shutil.rmtree(folder)
                    logger.debug(f"已清理临时目录: {folder}")
                except Exception as e:
                    logger.warning(f"清理 {folder} 失败: {e}")
    _cleaned = True

def signal_handler(signum, frame):
    global CLEANUP_TEMP
    logger.warning(f"接收到信号 {signum}，正在执行清理...")
    CLEANUP_TEMP = True
    cleanup_handler()
    sys.exit(0)

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_file(url, dest):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=os.path.basename(dest)) as t:
        urllib.request.urlretrieve(url, dest, reporthook=t.update_to)

def ensure_gfpgan_models():
    GFPGAN_WEIGHTS_DIR = Path(__file__).parent / "gfpgan" / "weights"
    GFPGAN_MODELS = {
        "detection_Resnet50_Final.pth": {
            "url": "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth",
            "desc": "人脸检测模型"
        },
        "parsing_parsenet.pth": {
            "url": "https://github.com/xinntao/facexlib/releases/download/v0.1.0/parsing_parsenet.pth",
            "desc": "人脸解析模型"
        }
    }
    GFPGAN_WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    for filename, info in GFPGAN_MODELS.items():
        if not (GFPGAN_WEIGHTS_DIR / filename).exists():
            missing.append((filename, info))
    if not missing:
        logger.info("GFPGAN 模型已存在")
        return True
    logger.warning(f"缺失 {len(missing)} 个 GFPGAN 模型，开始下载...")
    for filename, info in missing:
        dest = GFPGAN_WEIGHTS_DIR / filename
        logger.info(f"下载 {info['desc']}: {filename}")
        try:
            download_file(info["url"], str(dest))
            logger.info(f"下载完成: {filename}")
        except Exception as e:
            logger.error(f"下载失败 {filename}: {e}")
            return False
    return True

def main():
    global CLEANUP_TEMP
    parser = argparse.ArgumentParser(description="ReVox: 稳定版数字人管线 V1.0")
    parser.add_argument("--source_image", type=str, help="输入人脸图片")
    parser.add_argument("--driven_audio", type=str, help="驱动音频")
    parser.add_argument("--output_dir", type=str, default="results", help="成果输出目录")
    parser.add_argument("--upscale", action="store_true", help="开启画面增强")
    parser.add_argument("--method", choices=["fast", "face_fix"], help="增强模式")
    parser.add_argument("--keep_temp", action="store_true", help="保留临时缓存文件")
    parser.add_argument("--config", type=str, help="自定义配置文件路径")
    args = parser.parse_args()
    config_file = args.config if args.config else None
    config = ConfigManager(config_file=config_file, cli_args=args)
    atexit.register(cleanup_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    garbage_files = []
    final_video_path = None
    CLEANUP_TEMP = not args.keep_temp
    secure_ops = SecureFileOperations()
    try:
        check_ffmpeg_env()
        source_image = args.source_image or config.get("paths.source_image")
        driven_audio = args.driven_audio or config.get("paths.driven_audio")
        output_base = args.output_dir
        method = args.method or config.get("enhancements.method", "fast")
        if not source_image or not driven_audio:
            raise ReVoxError("缺少必要的输入文件参数")
        if not safe_path_check(source_image):
            raise ReVoxError(f"非法的源图像路径: {source_image}")
        if not safe_path_check(driven_audio):
            raise ReVoxError(f"非法的驱动音频路径: {driven_audio}")
        if not safe_path_check(output_base):
            raise ReVoxError(f"非法的输出目录路径: {output_base}")
        allowed_image_types = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        allowed_audio_types = ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']
        if not validate_file_type(source_image, allowed_image_types):
            raise ReVoxError(f"不支持的图像文件类型: {source_image}")
        if not validate_file_type(driven_audio, allowed_audio_types):
            raise ReVoxError(f"不支持的音频文件类型: {driven_audio}")
        secure_ops.secure_mkdir(output_base, parents=True, exist_ok=True)
        for folder in TEMP_FOLDERS:
            secure_ops.secure_mkdir(folder, parents=True, exist_ok=True)
        logger.info(">>> 环节 1: 输入素材标准化...")
        std_image = secure_ops.secure_join("temp_revox", "std_face.png")
        resize_and_pad(source_image, std_image)
        logger.info(">>> 环节 2: 启动 SadTalker 推理...")
        raw_video = run_sadtalker(std_image, driven_audio, config)
        base_name = sanitize_filename(os.path.basename(source_image).split('.')[0])
        timestamp = time.strftime("%H%M%S")
        if args.upscale or config.get("enhancements.superres"):
            logger.info(f">>> 环节 3: 执行 {method} 模式增强...")
            enhanced_temp = secure_ops.secure_join("temp_revox", f"enhanced_{timestamp}.mp4")
            run_video_upscale(raw_video, enhanced_temp, config, method=method)
            logger.info(">>> 环节 4: 执行最终音画重组...")
            save_name = f"revox_{base_name}_{timestamp}.mp4"
            target_path = secure_ops.secure_join(output_base, save_name)
            final_video_path = merge_audio_video(enhanced_temp, driven_audio, target_path)
        else:
            logger.info(">>> 跳过增强，正在迁移原始推理成果...")
            save_name = f"raw_{base_name}_{timestamp}.mp4"
            target_path = secure_ops.secure_join(output_base, save_name)
            shutil.copy(raw_video, target_path)
            final_video_path = target_path
        logger.info(">>> 环节 5: 获取生成视频信息...")
        print_video_info(final_video_path)
        logger.info(f"流程圆满结束！成果文件已存至: {final_video_path}")
    except ReVoxError as e:
        logger.error(f"运行失败: {e}")
    except KeyboardInterrupt:
        logger.warning("用户中断操作")
    except Exception as e:
        logger.critical(f"系统崩溃: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())
    finally:
        if CLEANUP_TEMP:
            cleanup_handler()

if __name__ == "__main__":
    main()
