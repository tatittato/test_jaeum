from fastapi import APIRouter, File, UploadFile, Depends,Form
from datetime import datetime
import cv2
import mediapipe as mp
import os
from fastapi_app.utils.pose_recognize.classify_pose import classify_pose
from fastapi_app.utils.pose_recognize.detect_pose import detect_pose
from fastapi_app.utils.pose_recognize.detect_face import detect_face

from ..database import SessionLocal, engine

from ..crud import *
from ..schemas import *
from ..model import *
from sqlalchemy.orm import Session

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()



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
        labels_str = ''.join(labels)

        # 라벨링 되기 전 이미지는 삭제합니다.
        if os.path.exists(file_path):
            os.remove(file_path)

        return labels_str


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
        event_data_path=file_path
    )

    db_sleep_event = create_sleep_event(db, sleep_event_data)

    return "Image saved successfully with pixelation"



# 사용자 생성
@router.post("/record/create_user")
async def create_user(user: UserBase, db: Session = Depends(get_db)):

    db_user = create_db_user(db, user)
    
    return db_user

# 수면 정보 생성
@router.post("/record/create_sleep_info", response_model=SleepInfoBase)
async def create_sleep_info(sleep_info: SleepInfoBase, db: Session = Depends(get_db) ):

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

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8000)
   
