def body_direction (nose_landmark_z, shoulder_left_z, shoulder_right_z ):

    if (shoulder_left_z > nose_landmark_z > shoulder_right_z):
        return ("right")
    if (shoulder_left_z < nose_landmark_z < shoulder_right_z):
        return ("left")   
    if ((shoulder_left_z < nose_landmark_z) and (shoulder_right_z < nose_landmark_z)) :
        return ("prone")
    if ((shoulder_left_z > nose_landmark_z) and (shoulder_right_z > nose_landmark_z)):
        return ("front")


def is_raise_arm(right_shoulder_angle, left_shoulder_angle, right_elbow_angle, left_elbow_angle):
    result = []

    # 오른팔 오버헤드
    if (90 < left_shoulder_angle < 180) and left_elbow_angle < 70:
        result.append("overhead Pose - left arm")
    # 오른팔 만세
    elif 70 < left_shoulder_angle < 180:
        result.append("manse pose - left arm")
    # 왼팔 오버헤드
    if (90 < right_shoulder_angle < 180) and right_elbow_angle < 70:
        result.append("overhead Pose - right arm")
    # 왼팔 만세
    elif 70 < right_shoulder_angle < 180:
        result.append("manse pose - right arm")
    # 양팔 오버헤드
    if (
        (90 < left_shoulder_angle < 180)
        and (90 < right_shoulder_angle < 180)
        and (left_elbow_angle < 70)
        and (right_elbow_angle < 70)
    ):
        result.append("overhead pose - all arms")
        
    # 양팔 만세 (양팔 오버헤드가 아닐 때만 포함)
    if (
        "overhead pose - all arms" not in result
        and "manse pose - left arm" in result
        and "manse pose - right arm" in result
    ):
        result.append("manse pose - all arms")
    
    if "manse pose - left arm" in result and "manse pose - right arm" in result and "manse pose - all arms" in result:
        return "manse"
    elif "overhead pose - all arms" in result or "overhead Pose - left arm" in result or "overhead Pose - right arm" in result:
        return "overhead"
    else:
        return False


def is_folded_legs(left_knee_angle, right_knee_angle):
    if (right_knee_angle < 90 or 240 < right_knee_angle) and (left_knee_angle < 90 or 240 < left_knee_angle):
        return 'folded - all'
    elif (right_knee_angle < 90 or 240 < right_knee_angle):
        return 'folded - right'
    elif (left_knee_angle < 90 or 240 < left_knee_angle):
        return 'folded - left'
    else:
        return None


def is_folded_hip(left_hip_angle, right_hip_angle):
    if right_hip_angle < 130 or left_hip_angle < 130:
        return True


def is_side (left_knee_angle, right_knee_angle,nose_landmark_z, shoulder_left_z, shoulder_right_z ):

    if body_direction(nose_landmark_z, shoulder_left_z, shoulder_right_z ) in ['right', 'left'] and is_folded_legs(left_knee_angle, right_knee_angle) != 'folded - all':
        return True


def is_shrimp(left_knee_angle, right_knee_angle, left_hip_angle, right_hip_angle):
    if is_folded_legs(left_knee_angle, right_knee_angle) == 'folded - all' and is_folded_hip(left_hip_angle, right_hip_angle):
        return True
    else:
        return False
    
# 무릎 세운 잠 ("prone 제외, 옆모습 제외해야될 듯")
def is_knee_up(left_knee_z, right_knee_z, labels):
  # (left_knee_z - right_knee_z)의 절대값
  z_diff = abs(left_knee_z - right_knee_z)  
  
  # 비교하려는 기준값 설정
  diff_threshold = 140  
  
  if "front" in labels:
    if z_diff > diff_threshold:
      # 차이가 140보다 크면 무릎 세운 잠 > True 반환
      return True
    else:
      return False

def is_cross_legs(left_hip_knee_angle, right_hip_knee_angle, labels):

  # 뒷모습 일 경우 (뒷모습 백숙함수 호출 및 함수결과 리턴) => 뒷모습일때는 백숙 불가한 것으로 간주한다ㅡㅡ
  if "prone" in labels:
    # return isCrossLegsProne(left_hip_knee_angle, right_hip_knee_angle, labels)
    return False
  # if "legs folded - all" not in labels:
  # 기준 각도가 너무 애매하다 => 다른 방법을 찾는 방안을 생각해보아요
  # if (270 < left_hip_knee_angle or 270 < right_hip_knee_angle):
  # if (275 < left_hip_knee_angle or 275 < right_hip_knee_angle):
  # labels.append("cross legs")	
  # return True
  else : pass

  # 옆모습일때는 백숙 아님
  if "front" in labels:
    if (80 >= left_hip_knee_angle or 80 >= right_hip_knee_angle):
      if all(label not in labels for label in ("folded - all", "knee up")):
      # 다리를 둘 다 접지않음 + 무릎좌표z의 차이가 140보다 작음: 무릎을 안세움 -> 백숙
        return True
      elif all(label in labels for label in("folded - all", "knee up")):
      # 다리를 둘 다 접음 + 무릎좌표z의 차이가 140보다 큼: 무릎을 세움 -> 백숙
        return True
  else: return False

# 정자세
def is_standard(angle_z_list, labels):

  # 정면이고
  if "front" in labels:

    # 오버헤드나 만세자세는 정자세 아님
    if is_raise_arm(angle_z_list['right_shoulder_angle'], angle_z_list['left_shoulder_angle'], 
                  angle_z_list['right_elbow_angle'], angle_z_list['left_elbow_angle']) != False :
       return False

    # 쉬림프는 정자세 아님
    if is_shrimp(angle_z_list['left_knee_angle'],angle_z_list['right_knee_angle'],
                angle_z_list['left_hip_angle'],angle_z_list['right_hip_angle']):
       return False
    
    # 양쪽 다리가 안 접혔으면 정자세 아님
    if is_folded_legs(angle_z_list['left_knee_angle'],angle_z_list['right_knee_angle']) == 'folded - all':
      return False
    
    # 허리가 접혔으면 정자세 아님
    if is_folded_hip(angle_z_list['left_hip_angle'], angle_z_list['right_hip_angle']):
       return False
    
    # 무릎을 세웠으면 정자세 아님
    if is_knee_up(angle_z_list['left_knee_z'], angle_z_list['right_knee_z'], labels):
       return False
    
    # 백숙은 정자세 아님
    if is_cross_legs(angle_z_list['left_hip_knee_angle'], angle_z_list['right_hip_knee_angle'], labels):
      return False
  
	# 위 if문에 해당하지 않으면 정자세를 리턴
    return True