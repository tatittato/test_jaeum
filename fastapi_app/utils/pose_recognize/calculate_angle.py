import math

#세 개의 랜드마크 (landmark1, landmark2, landmark3)를 입력으로 받아서 각도를 계산하는 역할
def calculate_angle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    #atan2 함수는 주어진 두 점 간의 아크탄젠트 값을 계산, 이를 이용하여 각도 산출
    #math.degrees 함수를 사용하여 각도를 도 단위로 변환
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    #계산된 각도가 0 미만일 경우, 360을 더하여 양수로 만들어 줌
    if angle < 0:
        angle += 360
    
    return angle