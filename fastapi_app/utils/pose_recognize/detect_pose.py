import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

#신체 랜드마크 감지를 위해 MediaPipe 포즈 모델을 초기화합니다.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

#mp_drawing 변수를 초기화하고 이를 mp.solutions.raw_utils 클래스와 연결
mp_drawing = mp.solutions.drawing_utils

def detect_pose(image, pose, display=True):
    #입력 이미지를 복사하여 output_image 변수에 저장
    output_image = image.copy()
    #입력 이미지를 BGR에서 RGB로 변환하여 imageRGB 변수에 저장합니다. 이것은 이미지의 색상 채널을 변경
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #변환된 이미지를 사용하여 포즈 객체 pose의 process 메서드를 호출하여 포즈를 감지하고 결과를 results 변수에 저장
    results = pose.process(imageRGB)
    #입력 이미지의 높이와 너비를 height와 width 변수에 저장
    height, width, _ = image.shape
    #저장할 빈 리스트 landmarks를 생성
    landmarks = []


    #포즈 결과에서 pose_landmarks가 존재하는지 확인
    if results.pose_landmarks:
        #이미지에 포즈 랜드마크를 그립니다.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)
        # 각 keypoint에 대한 confidence score 출력
        desired_landmarks = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

        # 랜드마크의 컨피던스 스코어 출력
        # for idx, landmark in enumerate(results.pose_landmarks.landmark):
        #     if idx in desired_landmarks:
        #         print(
        #             f"ID: {idx}, Visibility: {landmark.visibility}"
        #         )
        
        #포즈의 각 랜드마크에 대해 반복
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

    if display:
        plt.figure(figsize=[11, 11])
        #원본 이미지와 포즈 감지 결과를 두 개의 서브플롯에 표시
        plt.subplot(121); plt.imshow(image[:, :, ::-1]); plt.title("Original Image"); plt.axis('off');
        plt.subplot(122); plt.imshow(output_image[:, :, ::-1]); plt.title("Output Image"); plt.axis('off');
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
    else:
        return output_image, landmarks
    