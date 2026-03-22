import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import os
import soundfile as sf
import numpy as np
from src.utils.audio_utils import preprocess_audio
from src.enhancers.denoise import process_audio


class TestAudioPipeline(unittest.TestCase):
    def setUp(self):
        # 创建一个临时的测试音频文件 (1秒的正弦波 + 随机噪声)
        self.test_file = "test_input.wav"
        self.sample_rate = 44100
        t = np.linspace(0, 1, self.sample_rate)
        # 生成 440Hz 正弦波 + 噪声
        signal = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.randn(self.sample_rate)
        sf.write(self.test_file, signal, self.sample_rate)
        self.output_std = "test_std.wav"
        self.output_denoised = "test_denoised.wav"

    def tearDown(self):
        for f in [self.test_file, self.output_std, self.output_denoised]:
            if os.path.exists(f):
                os.remove(f)

    def test_01_preprocessing(self):
        print("\n测试音频标准化 (audio_utils)...")
        out = preprocess_audio(self.test_file, self.output_std, target_sr=16000)
        self.assertTrue(os.path.exists(out))
        # 验证采样率是否正确
        data, sr = sf.read(out)
        self.assertEqual(sr, 16000)
        print(f"采样率已成功转换: {sr}Hz")

    def test_02_denoising(self):
        print("\n测试音频降噪 (denoise)...")
        # 标准化
        std_audio = preprocess_audio(self.test_file, self.output_std, target_sr=16000)
        # 降噪
        out = process_audio(std_audio, self.output_denoised, prop_decrease=0.9)
        self.assertTrue(os.path.exists(out))
        # 验证降噪后能量是否减小
        original_data, _ = sf.read(std_audio)
        denoised_data, _ = sf.read(out)
        self.assertLess(np.var(denoised_data), np.var(original_data))
        print(f"降噪测试通过，能量分布已改变。")


if __name__ == '__main__':
    unittest.main()
