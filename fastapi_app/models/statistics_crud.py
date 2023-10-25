
from fastapi_app import model
from fastapi_app import schemas
import sqlalchemy
from sqlalchemy import between
from sqlalchemy.orm import Session

# statistics crud
# "기간별" 수면 시간정보 가져오기
def get_sleep_data(start, end, db:Session, response_model: schemas.SleepInfoBase):
  # 해당하는 날짜 정보만 가져오기 (between은 filter와 함께 쓴다)
  if start == None:
    # 전체 기간동안의 정보를 가져오기
    sleep_data = db.query(model.SleepInfo).filter(model.SleepInfo.date <= end).order_by(model.SleepInfo.date).all()
  else :
    # between 기간동안의 정보를 가져오기
    sleep_data = db.query(model.SleepInfo).filter(between(model.SleepInfo.date, start, end)).order_by(model.SleepInfo.date).all()
  
  sleep_data = [to_dict(item) for item in sleep_data] # 위에서 가져온 데이터를 딕셔너리로 변환
  return sleep_data


# "수면 이벤트정보도 가져오기"
def get_sleep_event_data(start, end, db:Session, response_model: schemas.SleepEventBase):
  sleep_event_data = []
  if start == None:
    # 전체 기간동안의 정보를 가져오기
    event_data = (db.query(model.SleepEvent, model.SleepInfo.date)
      .join(model.SleepInfo, model.SleepEvent.sleep_info_id == model.SleepInfo.sleep_info_id)
      .filter(model.SleepInfo.nickname == 'test')
      .filter(model.SleepInfo.date <= end)
      .distinct()  # 모든 컬럼 조합의 중복 제거
      .order_by(model.SleepEvent.sleep_event_id)
      .all())
  else: # between 기간동안의 정보를 가져오기
    event_data = (db.query(model.SleepEvent, model.SleepInfo.date)
      .join(model.SleepInfo, model.SleepEvent.sleep_info_id == model.SleepInfo.sleep_info_id)
      .filter(model.SleepInfo.nickname == 'test')
      .filter(between(model.SleepInfo.date, start, end))
      .distinct()  # 모든 컬럼 조합의 중복 제거
      .order_by(model.SleepEvent.sleep_event_id)
      .all())

  event_data = [tuple_to_dict(item) for item in event_data]
  sleep_event_data.extend(event_data)  # 각 항목의 쿼리 결과를 리스트에 추가  

  return sleep_event_data


# 데이터를 딕셔너리로 변환하는 함수
def to_dict(sleep_data):
  return {c.key: getattr(sleep_data, c.key) for c in sqlalchemy.inspect(sleep_data).mapper.column_attrs}


# 조인된 데이터를 딕셔너리로 변환하는 함수
def tuple_to_dict(data):
  sleep_event_dict = to_dict(data[0])
  sleep_event_dict["date"] = data[1]
  return sleep_event_dict