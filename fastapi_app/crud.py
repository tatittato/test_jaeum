
import sqlalchemy
from sqlalchemy import between
from sqlalchemy.orm import Session
import datetime

from fastapi_app import model
from fastapi_app import schemas

def create_db_user(db: Session, user: schemas.UserBase):
    db_user = model.User(nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_db_sleep_info(db: Session, sleep_info: schemas.SleepInfoBase):
    db_sleep_info = model.SleepInfo(
        nickname=sleep_info.nickname,
        start_sleep=sleep_info.start_sleep,
        end_sleep=sleep_info.end_sleep,
        total_sleep=sleep_info.total_sleep
    )
    print(type(sleep_info.nickname))
    db.add(db_sleep_info)
    db.commit()
    db.refresh(db_sleep_info)
    return db_sleep_info


# statistics crud
# "기간별" 수면 시간정보 가져오기
def get_sleep_data(start, end, db:Session, response_model: schemas.SleepInfoBase):

    # 해당하는 날짜 정보만 가져오기 (between은 filter와 함께 쓴다)
    # sleep_data = db.query(model.SleepInfo).filter_by(date='2023-10-19').all()
    sleep_data = db.query(model.SleepInfo).filter(between(model.SleepInfo.date, start, end))
    sleep_data = [to_dict(item) for item in sleep_data]
    
    print("sleep_data => ", sleep_data)
    return sleep_data

def to_dict(sleep_data):
    return {c.key: getattr(sleep_data, c.key) for c in sqlalchemy.inspect(sleep_data).mapper.column_attrs}
