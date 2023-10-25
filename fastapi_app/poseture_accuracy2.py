
import cv2
import mediapipe as mp
# from music import play_random_music
from datetime import datetime
import time
import os
# 함수 import
from utils.pose_recognize.classify_pose import classify_pose
from utils.pose_recognize.detect_pose import detect_pose

#신체 랜드마크 감지를 위해 MediaPipe 포즈 모델을 초기화합니다.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
pose_video = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=1)


# 이미지 파일이 있는 폴더 경로
image_folder = 'static/images/Pose/shrimp'

# 이미지 파일 경로 목록을 저장할 리스트 초기화
image_paths = []

# 폴더 내의 파일 순회
for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif')):
        # 이미지 파일 확장자인 경우에만 리스트에 추가하면서 정렬
        image_path = os.path.join(image_folder, filename)
        image_paths.append(image_path)

# 이미지 파일 경로를 오름차순으로 정렬
image_paths.sort()

print("이미지",image_paths)
# Create a named window
cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)

# 반환받을 라벨을 저장할 리스트
returned_label = []

# 밝기, 대비 조절 적용
for image_path in image_paths:
    frame = cv2.imread(image_path)

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ =  frame.shape
    frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
    frame, landmarks = detect_pose(frame, pose_video, display=False)
    fps = 50


    if landmarks:
        frame, labels = classify_pose(landmarks, frame, fps, frame_height, frame_width, display=False)
        returned_label.append(labels)
        print('labels => ', labels)
        print('returned_label => ', returned_label)
        


    cv2.imshow('Pose Classification', frame)
    k = cv2.waitKey(1) & 0xFF

    # 1초에 1프래임씩 찍음
    time.sleep(1)

    # ESC로 종료
    if(k == 27):
        break

#모든 OpenCV 표시 창을 닫습니다.
cv2.destroyAllWindows()

# play_random_music()

# 라벨을 지정합니다.
specified_labels = ["shrimp - right"]
print(specified_labels)
# Initialize a variable to count correct matches
correct_matches = 0


# 반환받은 라벨리스트 안에 있는 리스트 개수만큼 반복
for label in returned_label:
  # 안에 든 리스트의 길이만큼 i를 반복해서 인덱스에 있는 값과 specified label의 값을 비교함
  for i in range(len(label)):
    if label[i] in specified_labels:
        correct_matches += 1

# 일치도를 계산합니다.
percentage_match = (correct_matches / len(returned_label)) * 100

print(f"Percentage of matches: {percentage_match:.2f}%")

