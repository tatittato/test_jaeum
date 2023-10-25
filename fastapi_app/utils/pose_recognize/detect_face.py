import cv2
import mediapipe as mp

# 미디어파이프 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.30)

def detect_face(image, factor=15):
    # RGB 이미지로 변환
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 얼굴 감지 수행
    results = face_detection.process(frame_rgb)
    
    if results.detections:
        for detection in results.detections:
            # 감지된 얼굴의 바운딩 박스 정보 가져오기
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            # 얼굴 주위에 픽셀화 적용
            # 얼굴 영역 크기 조정
            face_roi = image[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (0, 0), fx=0.04, fy=0.04)  # 얼굴 크기 축소
            face_roi = cv2.resize(face_roi, (w, h), interpolation=cv2.INTER_NEAREST)  # 원래 크기로 확대
            image[y:y+h, x:x+w] = face_roi  # 원본 이미지에 픽셀화된 얼굴 영역 적용

    return image
