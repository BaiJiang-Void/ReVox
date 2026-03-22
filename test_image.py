import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import os
import cv2
import numpy as np
from src.utils.image_utils import resize_and_pad


class TestImageUtils(unittest.TestCase):
    def setUp(self):
        self.test_img = "test_input.jpg"
        self.output_img = "test_standard.png"
        # 创建一个随机的长方形图片
        random_img = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
        cv2.imwrite(self.test_img, random_img)

    def tearDown(self):
        for f in [self.test_img, self.output_img]:
            if os.path.exists(f):
                os.remove(f)

    def test_resize_padding(self):
        print("\n测试图片缩放与填充 (image_utils)...")
        out = resize_and_pad(self.test_img, self.output_img, target_size=(512, 512))
        self.assertTrue(os.path.exists(out))
        img = cv2.imread(out)
        self.assertEqual(img.shape[0], 512)
        self.assertEqual(img.shape[1], 512)
        print(f"图片标准化成功: 800x600 -> {img.shape[1]}x{img.shape[0]}")


if __name__ == '__main__':
    unittest.main()
