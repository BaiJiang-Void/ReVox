#!/bin/bash
# 定位 SadTalker 目录
SADTALKER_PATH="../../SadTalker"
if [ ! -d "$SADTALKER_PATH" ]; then
    echo "错误: 未能在 $SADTALKER_PATH 找到 SadTalker 目录"
    exit 1
fi
echo "正在准备 SadTalker 权重目录..."
mkdir -p "$SADTALKER_PATH/checkpoints"
mkdir -p "$SADTALKER_PATH/gfpgan/weights"
echo "正在下载核心模型 epoch_20.pth..."
curl -L -o "$SADTALKER_PATH/checkpoints/epoch_20.pth" "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar"
echo "正在下载 GFPGAN 权重..."
curl -L -o "$SADTALKER_PATH/gfpgan/weights/alignment_WFLW_4HG.pth" "https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth"
echo "权重准备就绪！"