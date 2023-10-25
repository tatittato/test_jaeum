import cv2
import mediapipe as mp
import os
import time
from fastapi_app.utils.pose_recognize.classify_pose import classify_pose
from fastapi_app.utils.pose_recognize.detect_pose import detect_pose

# 신체 랜드마크 감지를 위해 MediaPipe 포즈 모델을 초기화합니다.
mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

# 상위 폴더 설정
parent_folder = 'Pose'

# 정답지와 예측 배열 초기화
ground_truth = []
predicted_labels = []

# 상위 폴더 내의 폴더 순회
for folder_name in os.listdir(parent_folder):
    folder_path = os.path.join(parent_folder, folder_name)

    if os.path.isdir(folder_path):
        # 폴더 이름을 라벨로 사용
        label = folder_name

        # 해당 폴더 내의 이미지 파일 목록을 가져오기
        image_paths = []
        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(folder_path, filename)
                image_paths.append(image_path)

        # 이미지 파일 경로를 오름차순으로 정렬
        image_paths.sort()

        # 이미지 파일을 순회하면서 라벨 할당
        for image_path in image_paths:
            frame = cv2.imread(image_path)

            # 좌우 반전
            frame = cv2.flip(frame, 1)

            frame_height, frame_width, _ = frame.shape
            frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
            frame, landmarks = detect_pose(frame, pose_video, display=False)
            fps = 50

            if landmarks:
                frame, labels = classify_pose(landmarks, frame, fps, frame_height, frame_width, display=False)

                # 정답지와 예측 배열에 라벨 추가
                ground_truth.append(label)
                predicted_labels.append(labels)

            print("정답지",ground_truth)
            print("예측지",predicted_labels)

            cv2.imshow('Pose Classification', frame)
            k = cv2.waitKey(1) & 0xFF
            time.sleep(1)

            if k == 27:
                break

# 모든 OpenCV 표시 창을 닫습니다.
cv2.destroyAllWindows()

# 정확도 계산
correct_matches = sum(1 for true_label, predicted_label in zip(ground_truth, predicted_labels) if true_label in predicted_label)
accuracy = (correct_matches / len(ground_truth)) * 100

print(f"Percentage of matches: {accuracy:.2f}%")
