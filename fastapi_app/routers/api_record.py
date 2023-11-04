from fastapi import APIRouter, File, UploadFile, Depends,Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json
import cv2
import mediapipe as mp
import os
from fastapi_app.utils.pose_recognize.classify_pose import classify_pose
from fastapi_app.utils.pose_recognize.detect_pose import detect_pose
from fastapi_app.utils.pose_recognize.detect_face import detect_face
from fastapi_app.utils.openai_prompt import generate_sleep_feedback
from ..database import SessionLocal, engine

from ..crud import *
from ..schemas import *
from ..model import *
from sqlalchemy.orm import Session

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

templates = Jinja2Templates(directory="templates")


# "Record"라는 태그를 가지며, 404 응답 코드에 대한 설명도 정의
router = APIRouter(
    tags=["Record"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def process_image(image):
    # 이미지를 캡처하고 저장합니다.
    file_path = f"static/images/pose/{image.filename}"
    with open(file_path, "wb") as image_file:
        image_file.write(image.file.read())

    # 캡처한 이미지를 읽습니다.
    image = cv2.imread(file_path)

    # 랜드마크를 감지합니다.
    response = detect_pose(image, pose, display=False)

    if response is not None:
        landmarks_image, landmarks = response
        frame_height, frame_width, _ = landmarks_image.shape
        fps = 50

        # 랜드마크를 기반으로 레이블을 분류합니다.
        labeled_image, labels = classify_pose(landmarks, landmarks_image, fps, frame_height, frame_width, display=False)

        # 배열을 문자열로 바꾸기
        labels_str = ' '.join(labels)

        # 라벨링 되기 전 이미지는 삭제합니다.
        if os.path.exists(file_path):
            os.remove(file_path)

        return labels_str
    

def calculate_bad_sleep_without_event(sleep_events, event_times, end_sleep, event_to_exclude):
    bad_sleep_duration = datetime.strptime("00:00:00", '%H:%M:%S')  # '나쁜' 수면 시간을 추적하는 변수 초기화
    i = 0
    while i < len(sleep_events):
        # 이벤트가 제외할 이벤트와 일치하는지 확인
        if sleep_events[i] == event_to_exclude:
            i += 1
            continue
        
        # 만약 마지막 이벤트라면 end_sleep 시간까지의 기간 계산
        if i == len(sleep_events) - 1:
            event_duration = datetime.strptime(end_sleep, '%H:%M:%S') - datetime.strptime(event_times[i], '%H:%M:%S')
        else:
            # 연이어 일어난 이벤트 간의 기간 계산
            event_duration = datetime.strptime(event_times[i + 1], '%H:%M:%S') - datetime.strptime(event_times[i], '%H:%M:%S')
        
        # 이벤트 기간을 나쁜 수면 시간에 더함
        bad_sleep_duration += event_duration
        
        # 다음 이벤트로 이동하되, 제외할 이벤트라면 그 다음 이벤트를 건너뜀
        i += 2 if i < len(sleep_events) - 2 and sleep_events[i + 2] != event_to_exclude else 1

    return str(bad_sleep_duration.time())  # 시간 부분만 문자열로 반환

# 예를 들어, sleep_events와 event_times, end_sleep가 주어진 경우
# bad_position_time = calculate_bad_sleep_without_event(sleep_events, event_times, end_sleep, "front standard")
# bad_position_time = str(bad_position_time)
# 이제 bad_position_time은 '%H:%M:%S' 형식의 문자열로 반환될 것입니다.







@router.post("/record/return_posture")
async def upload_image(image: UploadFile):
    # 이미지 처리 함수 호출
    labels_str = process_image(image)  # 라벨 문자열 반환

    return labels_str


@router.post("/record/event_save")
async def event_image_save(image: UploadFile, data: str = Form(...), sleep_info_id: int = Form(...), db: Session = Depends(get_db)):
    # 현재 날짜와 시간 생성
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    formatted_time = datetime.now().strftime("%H-%M-%S")

    # 파일 저장 이름 정의
    file_path = f"static/images/pose/{current_date}_{formatted_time}_{data}.jpg"
    
    # DB 저장 이름 정의
    db_file_path = f"{current_date}_{formatted_time}_{data}.jpg"

    with open(file_path, "wb") as image_file:
        image_file.write(image.file.read())

    # 이미지 로드
    image = cv2.imread(file_path)

    # 얼굴 감지 및 픽셀화 처리 함수 호출
    image = detect_face(image, factor=15)

    # 픽셀화 처리한 이미지 저장
    cv2.imwrite(file_path, image)

    sleep_event_data = SleepEventBase(
        sleep_info_id=sleep_info_id,
        sleep_event=data,
        event_time=current_time,
        event_data_path=db_file_path
    )

    db_sleep_event = create_sleep_event(db, sleep_event_data)

    return "Image saved successfully with pixelation"



# 사용자 생성
@router.post("/record/create_user")
async def create_user(user: UserBase, db: Session = Depends(get_db)):

    db_user = create_db_user(db, user)
    
    return db_user

# 수면 정보 생성
@router.post("/record/create_sleep_info", response_model=SleepInfoCreate)
async def create_sleep_info(sleep_info: SleepInfoCreate, db: Session = Depends(get_db) ):

    db_sleep_info = create_db_sleep_info(db, sleep_info)
   
    return db_sleep_info

#수면 정보 아이디 가져오기
@router.post("/record/get_info_id")
async def get_info_id(request_data: SleepInfoIdGet, db: Session = Depends(get_db)):
    sleep_info_id = get_sleep_info_id(db, request_data.nickname)
    return sleep_info_id
    
# 수면 정보 업데이트
@router.put("/record/update/{nickname}", response_model=SleepInfoUpdate)
def update_sleep_info(nickname: str, sleep_info_data: SleepInfoUpdate, db: Session = Depends(get_db)):
    
    updated_sleep_info = update_info(db, nickname, sleep_info_data.total_sleep, sleep_info_data.end_sleep)
   
    return updated_sleep_info
    
# 수면 점수 업데이트
@router.put("/record/update/score/{nickname}", response_model=SleepInfoScoreUpdate)
def update_sleep_score_info(nickname: str, sleep_score_info_data : SleepInfoScoreUpdate, db : Session=Depends(get_db)):

    update_sleep_score_info = update_score_info(db, nickname, sleep_score_info_data.total_sleep_score, sleep_score_info_data.sleep_time_score,
                                                      sleep_score_info_data.start_sleep_time_score,  sleep_score_info_data.bad_position_score, sleep_score_info_data.position_change_score)

    return update_sleep_score_info

@router.post("/record/info_and_event")
async def get_info_and_events(request_data: RequestData, db: Session = Depends(get_db) ):
    db_info_event_data = get_sleep_info_with_events_by_nickname_and_id(
        db, request_data.nickname, request_data.sleep_info_id
    )
    
    results = SleepInfoGet(total_sleep='', start_sleep='',end_sleep='', sleep_event=[], event_time=[])
    sleep_events = []
    event_times = []
    for info in db_info_event_data:
        results.total_sleep = info.total_sleep
        results.start_sleep = info.start_sleep
        results.end_sleep = info.end_sleep
        sleep_events.append(info.sleep_event)
        event_times.append(info.event_time)
    
    results.sleep_event = sleep_events
    results.event_time = event_times

    bad_position_time = calculate_bad_sleep_without_event(sleep_events, event_times, results.end_sleep, "front standard")

     # results 데이터를 JSON 형식으로 변환
    results_json = {
        "total_sleep": results.total_sleep,
        "start_sleep": results.start_sleep,
        "sleep_event": results.sleep_event,
        "bad_position_time": bad_position_time
    }
    json_data = json.dumps(results_json)
    print("gpt한테 보내주는 값: ", type(json_data))
    # generate_sleep_feedback 함수에 results_text를 전달하여 GPT-3.5 모델에 데이터를 제공
    response = generate_sleep_feedback(json_data)
    feedback = response["choices"][0]["message"]["content"].replace("\n", "<br>")
    
    return feedback

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8000)
   
