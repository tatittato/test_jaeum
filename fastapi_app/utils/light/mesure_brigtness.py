import cv2

# 밝기 측정 함수
def measure_brightness(frame):
    # 색상을 grayscale로 변환하여 밝기 계산
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = gray.mean()
    
    # 0~255 범위의 밝기를 1~10 범위의 정수로 정규화
    normalized_brightness = int(round((brightness / 255) * 99 + 1))
    return normalized_brightness
