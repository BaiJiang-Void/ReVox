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

信息提取：一键打印视频的相关信息，包括分辨率、帧率、时长等。

# 使用手册

命令行参数：

\--source\_image 用于手动输入人脸图片路径

\--driven\_audio 用于手动输入驱动音频路径

\--output\_dir 用于手动选择输出目录

\--upscale 用于手动选择是否开启画质增强

\--method 用于手动选择增强模式（需要配合 --upscale）

\--keep\_temp 用于决定是否保留临时文件

\--config 用于手动输入配置文件的路径

配置文件：

在config/default.yaml中存放着默认配置文件，系统在没有收到--config相关文件时会自动尝试调用默认配置文件。



