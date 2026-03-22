from setuptools import setup, find_packages

setup(
    name="ReVox",
    version="0.1.0",
    description="基于 SadTalker 的音视频增强全流程工具 (Denoise & SuperRes)",
    author="BaiJiang-Void",
    url="https://github.com/BaiJiang-Void/ReVox",
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
            "revox = src.cli:main",
        ],
    },
    python_requires=">=3.8",
)