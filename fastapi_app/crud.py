
from sqlalchemy.orm import Session


from sqlalchemy import func
from fastapi_app import model
from fastapi_app import schemas

def create_db_user(db: Session, user: schemas.UserBase):
    db_user = model.User(nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_sleep_info_id(db: Session, nickname: str):
    sleep_info_id = (
        db.query(model.SleepInfo)
        .filter(model.SleepInfo.nickname == nickname)
        .order_by(model.SleepInfo.sleep_info_id.desc())
        .first()
    )

        
    return sleep_info_id
    
def create_db_sleep_info(db: Session, sleep_info: schemas.SleepInfoBase):
    
    db_sleep_info = model.SleepInfo(
        nickname=sleep_info.nickname,
        start_sleep=sleep_info.start_sleep,
    )
    print(type(sleep_info.nickname))
    db.add(db_sleep_info)
    db.commit()
    db.refresh(db_sleep_info)
    return db_sleep_info


def update_info(db: Session, nickname: str, total_sleep: str, end_sleep: str):
    # 가장 마지막 sleep_info_id 가져오기
    latest_sleep_info_id = db.query(func.max(model.SleepInfo.sleep_info_id)).filter(model.SleepInfo.nickname == nickname).scalar()

    if latest_sleep_info_id is not None:
        # 해당 sleep_info_id를 사용하여 업데이트
        db_sleep_info = db.query(model.SleepInfo).filter(model.SleepInfo.sleep_info_id == latest_sleep_info_id).first()
        if db_sleep_info:
            db_sleep_info.total_sleep = total_sleep
            db_sleep_info.end_sleep = end_sleep
            db.commit()
            db.refresh(db_sleep_info)
            return db_sleep_info

def update_score_info(db: Session, nickname: str, total_sleep_score : int, sleep_time_score: int, start_sleep_time_score: int, bad_position_score: int, position_change_score: int):
    
    latest_sleep_info_id = db.query(func.max(model.SleepInfo.sleep_info_id)).filter(model.SleepInfo.nickname == nickname).scalar() 


    if latest_sleep_info_id is not None:
            # 해당 sleep_info_id를 사용하여 업데이트
            db_sleep_info = db.query(model.SleepInfo).filter(model.SleepInfo.sleep_info_id == latest_sleep_info_id).first()
            if db_sleep_info:
                db_sleep_info.total_sleep_score = total_sleep_score
                db_sleep_info.sleep_time_score = sleep_time_score
                db_sleep_info.start_sleep_time_score = start_sleep_time_score
                db_sleep_info.bad_position_score = bad_position_score
                db_sleep_info.position_change_score = position_change_score
                db.commit()
                db.refresh(db_sleep_info)
                return db_sleep_info

def create_sleep_event(db: Session, sleep_event_data: schemas.SleepEventBase):
    db_sleep_event = model.SleepEvent(
        sleep_info_id=sleep_event_data.sleep_info_id,
        sleep_event=sleep_event_data.sleep_event,
        event_time=sleep_event_data.event_time,
        event_data_path=sleep_event_data.event_data_path,
    )
    db.add(db_sleep_event)
    db.commit()
    db.refresh(db_sleep_event)
    return db_sleep_event



