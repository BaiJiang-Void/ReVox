from setuptools import setup, find_packages

setup(
    name="ReVox",
    version="0.1.0",
    description="基于 SadTalker 的音视频增强全流程工具 (Denoise & SuperRes)",
    author="Your Name",
    url="https://github.com/BaiJiang-Void/ReVox",
    # 关键修复：直接查找 src 下的所有包
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "opencv-python",
        "numpy",
        "soundfile",
        "noisereduce",
        "torch",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            # 允许用户直接在终端输入 'revox' 来启动 cli
            "revox = src.cli:main",
        ],
    },
    python_requires=">=3.8",
)