import argparse
import sys
import os
# 确保项目根目录在 sys.path 中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.sadtalker_wrapper import run_sadtalker


def main():
    parser = argparse.ArgumentParser(description="ReVox: 基于 SadTalker 的全流程音视频增强工具")
    # 基础参数
    parser.add_argument("--image", required=True, help="源图片路径")
    parser.add_argument("--audio", required=True, help="驱动音频路径")
    parser.add_argument("--output", default="output.mp4", help="输出视频路径")
    # 渲染参数
    parser.add_argument("--size", type=int, choices=[256, 512], default=256, help="生成的分辨率 (256/512, 默认256以节省显存)")
    parser.add_argument("--still", action="store_true", help="静止模式（减少头部动作）")
    parser.add_argument("--enhancer", type=str, default=None, help="面部增强器")
    # 增强功能
    parser.add_argument("--denoise", action="store_true", help="启用音频降噪")
    parser.add_argument("--superres", action="store_true", help="启用视频超分放大")
    parser.add_argument("--scale", type=int, default=2, help="超分倍数 (默认2)")
    # 信息提取
    parser.add_argument("--info", action="store_true", help="打印视频元数据")
    parser.add_argument("--info_json", type=str, help="保存信息至 JSON")
    # 路径配置
    parser.add_argument("--sadtalker_path", type=str, help="SadTalker 目录路径")
    parser.add_argument("--sadtalker_python", type=str, help="SadTalker 环境 Python 路径")
    args = parser.parse_args()
    try:
        run_sadtalker(
            source_image=args.image,
            driven_audio=args.audio,
            output_path=args.output,
            size=args.size,
            still=args.still,
            enhancer=args.enhancer,
            denoise_flag=args.denoise,
            superres_flag=args.superres,
            superres_scale=args.scale,
            extract_info=args.info,
            info_json=args.info_json,
            sadtalker_path=args.sadtalker_path,
            sadtalker_python=args.sadtalker_python
        )
    except Exception as e:
        print(f"运行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
