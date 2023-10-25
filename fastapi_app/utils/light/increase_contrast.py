import cv2
from PIL import Image, ImageEnhance
import numpy as np

# 대비 조절 함수
def increase_contrast(img, factor):
    pil_img = Image.fromarray(img)
    enhancer = ImageEnhance.Contrast(pil_img)
    enhanced_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(enhanced_img), cv2.COLOR_RGB2BGR)