import cv2
import numpy as np
from PIL import Image, ImageEnhance

# 밝기 조절 함수
def increase_brightness(img, factor):
    # PIL 이미지로 변환 후 밝기 조절
    pil_img = Image.fromarray(img)
    enhancer = ImageEnhance.Brightness(pil_img)
    brighter_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(brighter_img), cv2.COLOR_RGB2BGR)