# ReVox (Audio-Visual Lip-Sync Enhancer)

ReVox 是一个基于 SadTalker 的全流程增强工具，旨在通过自动化预处理（降噪、缩放）和后处理（视频超分、元数据提取）来提升 AI 数字人生成的质量和易用性。

# 目录：

###### 快速开始

###### 详细安装指南

###### 核心功能

###### 使用手册

###### API 参考

###### 常见问题 (FAQ)

# 快速开始

准备环境：首先需要确保已经安装了FFmpeg并且在系统路径中，然后在cmd中输入命令。

&#x09;git clone https://github.com/BaiJiang-Void/ReVox.git

&#x09;cd ReVox

&#x09;pip install -r requirements.txt

运行示例：

&#x09;python -m src.cli --image examples/man.png --audio examples/LipTest.wav --size 256 --superres

# 详细安装指南

依赖项说明：

FFmpeg：必须安装，ReVox会使用它进行音视频合并。

SadTalker：ReVox会自动在同级目录寻找 SadTalker/。请确保 SadTalker/checkpoints/ 下有预训练权重。

权重配置：建议将权重文件夹命名为 checkpoints（复数），并包含以下关键文件。

&#x09;epoch\_20.pth

&#x09;BFMT\_model\_latest.pth

&#x09;gfpgan/weights/

# 核心功能

智能降噪：调用 noisereduce 算法，在生成视频前自动净化背景噪音。

自动适配：自动将输入图片缩放并填充至 256/512 尺寸，避免 SadTalker 报错。

视频超分：针对低显存用户，支持 256 模式生成后通过插值算法放大回高清尺寸。

元数据提取：一键导出视频的编码、分辨率及帧率信息至 JSON。

# 使用手册

标准生成：python -m src.cli --image image\_test.png --audio audio\_test.wav

低显存模式：python -m src.cli --image i.png --audio a.wav --size 256 --superres

高质量降噪：python -m src.cli --image i.png --audio a.wav --denoise

静止模式：python -m src.cli --image i.png --audio a.wav --still

参数说明：

\--size: 生成视频的基础分辨率 (256/512)。6GB 显存建议选 256。

\--superres: 是否在渲染后执行超分辨率放大。

\--scale: 超分倍数，默认 2。

\--sadtalker\_path: 手动指定 SadTalker 的安装路径。

# API参考

如果想要在Python脚本中调用ReVox，可以使用run\_sadtalker接口：

from src import run\_sadtalker

run\_sadtalker(

&#x20;   source\_image="path/to/img.png",

&#x20;   driven\_audio="path/to/audio.wav",

&#x20;   output\_path="output.mp4",

&#x20;   denoise\_flag=True,

&#x20;   superres\_flag=True,

&#x20;   size=256

)

# 常见问题

Q: 遇到 CUDA Out of Memory (OOM) 怎么办？

A: 这是显存不足。请务必使用 --size 256 参数。如果开启了浏览器或其他显存占用程序，请先关闭。

# 贡献与感谢

基于 SadTalker 开源项目。

感谢所有贡献者。

# 

