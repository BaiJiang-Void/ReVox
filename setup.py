from setuptools import setup, find_packages

setup(
    name="ReVox",
    version="1.0.0",
    description="ReVox: 稳定版数字人管线 - 基于 SadTalker",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="BaiJiang-Void",
    author_email="your.email@example.com",
    url="https://github.com/BaiJiang-Void/ReVox",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "opencv-python>=4.5",
        "numpy>=1.19",
        "soundfile>=0.10",
        "torch>=1.9",
        "tqdm>=4.62",
        "PyYAML>=5.4",
        "librosa>=0.8",
        "scipy>=1.7",
    ],
    extras_require={
        "gpu": ["onnxruntime-gpu>=1.12"],
        "dev": ["pytest", "flake8", "black"],
    },
    entry_points={
        "console_scripts": [
            "revox = src.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="digital-human, sadtalker, video-enhancement, face-animation",
    project_urls={
        "Bug Reports": "https://github.com/BaiJiang-Void/ReVox/issues",
        "Source": "https://github.com/BaiJiang-Void/ReVox",
    },
)
