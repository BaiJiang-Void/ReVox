import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import os
import cv2
import numpy as np
from src.enhancers.superres import enhance_video
from src.utils.video_utils import get_video_specs


class TestVideoPipeline(unittest.TestCase):
    def setUp(self):
        self.test_video = "test_input.mp4"
        self.output_superres = "test_upscaled.mp4"
        # 创建一个 10 帧的空白测试视频 (128x128)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.test_video, fourcc, 20.0, (128, 128))
        for _ in range(10):
            frame = np.zeros((128, 128, 3), dtype=np.uint8)
            cv2.putText(frame, "Test", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(frame)
        out.release()

    def tearDown(self):
        for f in [self.test_video, self.output_superres]:
            if os.path.exists(f):
                os.remove(f)

    def test_superres_upscale(self):
        print("\n测试视频超分 (superres)...")
        scale = 2
        enhance_video(self.test_video, self.output_superres, scale=scale)
        self.assertTrue(os.path.exists(self.output_superres))
        specs = get_video_specs(self.output_superres)
        self.assertEqual(specs['width'], 128 * scale)
        self.assertEqual(specs['height'], 128 * scale)
        print(f"超分成功: 128x128 -> {specs['width']}x{specs['height']}")


if __name__ == '__main__':
    unittest.main()
