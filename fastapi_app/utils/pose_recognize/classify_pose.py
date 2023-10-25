
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

from .calculate_angle import calculate_angle
from .pose import *

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose

# frame_count 전역변수 선언
frame_count = 0


def classify_pose(landmarks, output_image, fps, frame_height, frame_width, display=False):
    labels = [] # Initialize an empty list for labels
    colors = []  # Initialize an empty list for colors

    global frame_count
# 필요 없음
    # # 코 좌표, x, y
    # nose_landmark = landmarks[mp_pose.PoseLandmark.NOSE.value]

    # # shoulder의 midpoint x, y, z 좌표
    # shoulder_x = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0] + landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]) / 2
    # shoulder_y = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1] + landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1]) / 2
    # shoulder_z = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][2] + landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][2]) / 2
    
    # # shoulder x, y, z 좌표를 담은 midpoints 리스트
    # midpoints = (shoulder_x, shoulder_y, shoulder_z)

    # 지윤님 엎드려잠을 위한 z 좌표들
    nose_landmark_z = landmarks[mp_pose.PoseLandmark.NOSE.value][2]
    shoulder_left_z = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][2]
    shoulder_right_z = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][2]
    
    # 다리를 세웠는가에 사용할 무릎 z 좌표들 (25,26)
    left_knee_z = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][2]
    right_knee_z = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][2]

    right_elbow_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]))
    
    left_elbow_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]))   
    
    right_shoulder_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]))

    left_shoulder_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]))

    left_knee_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]))

    right_knee_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]))
    
    left_hip_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]))

    right_hip_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]))
    
    left_body_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.NOSE.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]))
    
    right_body_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.NOSE],
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]))

    # 사용랜드마크 23, 24, 26
    left_hip_knee_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]))

    # 사용랜드마크 24, 23, 25
    right_hip_knee_angle = int(calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]))

    # 정자세 함수 호출용 딕셔너리
    angle_z_list = {'right_elbow_angle': right_elbow_angle, 'left_elbow_angle': left_elbow_angle, 
                  'right_shoulder_angle':right_shoulder_angle, 'left_shoulder_angle':left_shoulder_angle,
                  'left_knee_angle':left_knee_angle, 'right_knee_angle':right_knee_angle,
                  'left_hip_angle':left_hip_angle, 'right_hip_angle':right_hip_angle,
                  'left_body_angle':left_body_angle, 'right_body_angle':right_body_angle,
                  'left_hip_knee_angle':left_hip_knee_angle, 'right_hip_knee_angle':right_hip_knee_angle,
                  'left_knee_z':left_knee_z, 'right_knee_z':right_knee_z
                  }

    # 몸방향 함수 호출
    direction = body_direction(nose_landmark_z, shoulder_left_z, shoulder_right_z)
    if direction:
        labels.append(direction)

    # 만세포즈 / 오버헤드 -> 어깨, 팔꿈치로 분류
    raiseArm = is_raise_arm(right_shoulder_angle, left_shoulder_angle, right_elbow_angle, left_elbow_angle)
    if raiseArm:
        labels.append('raise_arm')

    # 옆으로 잠
    if is_side(left_knee_angle, right_knee_angle, nose_landmark_z, shoulder_left_z, shoulder_right_z):
        labels.append('side')
    
    # 새우잠 (다리랑 허리 접힌 함수를 요기서 호출한다)
    if is_shrimp(left_knee_angle, right_knee_angle, left_hip_angle, right_hip_angle):
        labels.append('shrimp')

    # 무릎세운 함수
    if is_knee_up(left_knee_z, right_knee_z, labels):
        labels.append("knee_up")
    else: pass

    # 백숙자세 함수
    if is_cross_legs(left_hip_knee_angle, right_hip_knee_angle, labels):
        labels.append("cross_legs")
    else: pass

    # 정자세 (자세 검사 가장 마지막 if 문)
    if is_standard(angle_z_list, labels):
        labels.append("standard")

    global frame_count
    frame_count += 1
    
    y = 30
    color = (0, 255, 0)
    # Define colors for each label
    for label in labels:
        colors.append((0, 255, 0))  # Green color for each label
        cv2.putText(output_image, label, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        y += 30

    if display:
        plt.figure(figsize=[10, 10])
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')
    else:
        return output_image, labels  # Return the list of labels