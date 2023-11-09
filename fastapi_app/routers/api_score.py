from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session 
from ..database import SessionLocal, engine
from ..crud import *
from ..schemas import *
from ..model import *
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from datetime import datetime, timedelta, date

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Score"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/score/{nickname}/{date}")
async def get_score(request: Request, nickname: str , date : date , db: Session = Depends(get_db)):

    total_sleep_score = db.query(model.SleepInfo.total_sleep_score).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()
    position_change_score = db.query(model.SleepInfo.position_change_score).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()
    bad_position_score = db.query(model.SleepInfo.bad_position_score).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()
    sleep_time_score = db.query(model.SleepInfo.sleep_time_score).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()
    start_sleep_time_score = db.query(model.SleepInfo.start_sleep_time_score).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()
    sleeptimeget = db.query(model.SleepInfo.total_sleep).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()
    starttimeget = db.query(model.SleepInfo.start_sleep).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()


    #나쁜 자세로 잔 시간 가져오기
    sleep_event = db.query(model.SleepEvent.sleep_event).\
        join(model.SleepInfo, model.SleepInfo.sleep_info_id == model.SleepEvent.sleep_info_id).\
        filter(model.SleepInfo.date == date, model.SleepInfo.nickname ==  nickname).all()

    sleep_event_time = db.query(model.SleepEvent.event_time).\
        join(model.SleepInfo, model.SleepInfo.sleep_info_id == model.SleepEvent.sleep_info_id).\
        filter(model.SleepInfo.date == date, model.SleepInfo.nickname ==  nickname).all()
    
    sleep_end_time = db.query(model.SleepInfo.end_sleep).filter(model.SleepInfo.nickname == nickname, model.SleepInfo.date == date).first()

    # 주어진 시간 형식을 24시간 형식으로 변환하는 함수
    def to_24_hour_format(time_row):
        time_str = str(time_row[0])  # 튜플의 첫 번째 요소를 문자열로 변환
        return datetime.strptime(time_str, '%H:%M:%S')

    # 주어진 시간 형식을 시간 단위로 변환하는 함수
    def get_hour(time_str):
        time = to_24_hour_format(time_str)
        return time.hour + time.minute / 60 + time.second / 3600

    # sleep_event와 각 이벤트의 시작 및 종료 시간
    sleep_event_names = sleep_event
    sleep_event_start_times = sleep_event_time

    event_durations = {}
    for i in range(len(sleep_event_names)):
            event = sleep_event_names[i]
            start_time = sleep_event_start_times[i]
            
            if i == len(sleep_event_names) - 1:
                end_time = sleep_end_time
            else:
                end_time = sleep_event_start_times[i + 1]


            start_hour = get_hour(start_time)
            end_hour = get_hour(end_time)

            if start_hour <= end_hour:
                duration = end_hour - start_hour
            else:
                duration = 24 - start_hour + end_hour

            event_durations[event] = duration

    
    total_duration = 0

    # 이벤트와 각 이벤트의 duration에 대한 정보가 있는 event_durations 딕셔너리 순회
    for event, duration in event_durations.items():
        # 'front standard' 이벤트가 아닌 경우에만 duration을 합산
        if 'front standard' not in event:
            total_duration += duration
 
    hours = total_duration
    time_delta = timedelta(hours=hours)

    # timedelta를 문자열로 변환하고, "00:00:00" 형식으로 출력
    time_str = str(time_delta)

    badpositiontime = time_str
    bad_tuple = (badpositiontime,)


    total_sleep_score = total_sleep_score[0]
    position_change_score = position_change_score[0]
    bad_position_score = bad_position_score[0]
    sleep_time_score = sleep_time_score[0]
    start_sleep_time_score = start_sleep_time_score[0]


    # 자세 바뀐 횟수 가져오기
    query = db.query(model.SleepInfo.sleep_info_id).\
        join(model.SleepEvent, model.SleepInfo.sleep_info_id == model.SleepEvent.sleep_info_id).\
        filter(model.SleepInfo.date == date, model.SleepInfo.nickname ==  nickname)

    # 결과의 개수를 정수로 얻기
    position_changes = len(query.all())


    def time_to_minutes(time):
        if time:
            sleeptime = time[0]
            hours, minutes, seconds = map(int, sleeptime.split(':'))
            total_minutes = hours * 60 + minutes
        else:
            total_minutes = 0

        return total_minutes


    def minutes_to_hours(minutes):
        if minutes is None:
            return 0.0

        hours = round(minutes / 60, 1)
        return hours
    
    def minutes_to_hours_and_minutes(minutes):
        if minutes is None:
            return 0, 0  # 기본값으로 0 시간, 0 분을 반환

        hours = minutes // 60  # 분을 시간으로 나누어 몫을 구합니다
        minutes = minutes % 60  # 분을 60으로 나누어 나머지를 분으로 설정합니다

        return hours, minutes

    sleep_minutes_get =  time_to_minutes(sleeptimeget)
    start_minutes_get = time_to_minutes(starttimeget)
    bad_position_minutes = time_to_minutes(bad_tuple)

    total_sleep_time = minutes_to_hours_and_minutes(sleep_minutes_get)
    start_sleep_time = minutes_to_hours_and_minutes(start_minutes_get)
    bad_position_time = minutes_to_hours_and_minutes(bad_position_minutes)

    total_sleep_time_hours = total_sleep_time[0]
    total_sleep_time_minutes = total_sleep_time[1]
    start_sleep_time_hours = start_sleep_time[0]
    start_sleep_time_minutes = start_sleep_time[1]
    bad_position_time_hours = bad_position_time[0]
    bad_position_time_minutes = bad_position_time[1]

    # 'sleep_feedback'이 'SleepInfo' 모델의 속성인 경우
    sleep_info_instance = db.query(model.SleepInfo).filter(
        model.SleepInfo.date == date,
        model.SleepInfo.nickname == nickname
    ).first()

    # 인스턴스에서 'sleep_feedback' 가져오기
    sleep_feedback = sleep_info_instance.sleep_feedback

    result = {

        "position_changes": position_changes,
        "total_sleep_time_hours":total_sleep_time_hours,
        "total_sleep_time_minutes":total_sleep_time_minutes,
        "start_sleep_time_hours" :start_sleep_time_hours,
        "start_sleep_time_minutes" : start_sleep_time_minutes,
        "bad_position_time_hours" : bad_position_time_hours,
        "bad_position_time_minutes" : bad_position_time_minutes,
        "total_sleep_score": total_sleep_score,
        "position_change_score": position_change_score,
        "bad_position_score": bad_position_score,
        "sleep_time_score": sleep_time_score,
        "start_sleep_time_score": start_sleep_time_score,
        "nickname": nickname,
        "sleep_feedback": sleep_feedback
    }

    print(result)
    return JSONResponse(content=result)


@router.get("/score/{nickname}")
async def calculate_score(request: Request, nickname: str , db: Session = Depends(get_db)):

    #잠잔 시간 가져오기 
    sleeptimeget = db.query(model.SleepInfo.total_sleep).filter(model.SleepInfo.nickname == nickname).order_by(desc(model.SleepInfo.sleep_info_id)).first()
    
    #잠든 시간 가져오기 
    starttimeget = db.query(model.SleepInfo.start_sleep).filter(model.SleepInfo.nickname == nickname).order_by(desc(model.SleepInfo.sleep_info_id)).first()

    #가장 최근 sleep_info_id
    max_sleep_info_id = db.query(model.SleepInfo.sleep_info_id)\
    .filter(model.SleepInfo.nickname == nickname)\
    .order_by(desc(model.SleepInfo.sleep_info_id))\
    .first()

    #자세가 바뀐 횟슈 가져오기
    sleep_event = db.query(model.SleepEvent.sleep_event)\
    .filter(max_sleep_info_id ==model.SleepEvent.sleep_info_id)\
    .all()

    #나쁜 자세로 잔 시간 가져오기
    sleep_event_time = db.query(model.SleepEvent.event_time)\
    .filter(max_sleep_info_id == model.SleepEvent.sleep_info_id)\
    .all()
    
    
    sleep_end_time = db.query(model.SleepInfo.end_sleep).filter(model.SleepInfo.nickname == nickname).order_by(desc(model.SleepInfo.sleep_info_id)).first()

    print(sleep_event, sleep_event_time ,sleep_end_time)



    # 주어진 시간 형식을 24시간 형식으로 변환하는 함수
    def to_24_hour_format(time_row):
        time_str = str(time_row[0])  # 튜플의 첫 번째 요소를 문자열로 변환
        return datetime.strptime(time_str, '%H:%M:%S')

    # 주어진 시간 형식을 시간 단위로 변환하는 함수
    def get_hour(time_str):
        time = to_24_hour_format(time_str)
        return time.hour + time.minute / 60 + time.second / 3600

    # sleep_event와 각 이벤트의 시작 및 종료 시간
    sleep_event_names = sleep_event
    sleep_event_start_times = sleep_event_time

    event_durations = {}
    for i in range(len(sleep_event_names)):
            event = sleep_event_names[i]
            start_time = sleep_event_start_times[i]
            
            if i == len(sleep_event_names) - 1:
                end_time = sleep_end_time
            else:
                end_time = sleep_event_start_times[i + 1]

            start_hour = get_hour(start_time)
            end_hour = get_hour(end_time)

            if start_hour <= end_hour:
                duration = end_hour - start_hour
            else:
                duration = 24 - start_hour + end_hour

            event_durations[event] = duration


    
    total_duration = 0

    # 이벤트와 각 이벤트의 duration에 대한 정보가 있는 event_durations 딕셔너리 순회
    for event, duration in event_durations.items():
            # 'standard' 이벤트가 아닌 경우에만 duration을 합산
        if 'front standard' not in event:
            total_duration += duration
 
    hours = total_duration
    time_delta = timedelta(hours=hours)

    # timedelta를 문자열로 변환하고, "00:00:00" 형식으로 출력
    time_str = str(time_delta)

    badpositiontime = time_str
    bad_tuple = (badpositiontime,)

    # 자세 바뀐 횟수 가져오기
    query = db.query(model.SleepInfo.sleep_info_id).\
        join(model.SleepEvent, model.SleepInfo.sleep_info_id == model.SleepEvent.sleep_info_id).\
        filter(model.SleepInfo.nickname == nickname)

    # 결과의 개수를 정수로 얻기
    position_changes = len(query.all())


    def time_to_minutes(time):
        sleeptime = time[0]
        if  sleeptime is not None:    
            hours, minutes, seconds = map(int, sleeptime.split(':'))
            total_minutes = hours * 60 + minutes
        else:
            total_minutes = 0

        return total_minutes


    def calculate_sleep_time_score(time):
        score = 0

        if 420 <= time <= 540:  # 7시간(420분)부터 9시간(540분)까지
            score += 25
        elif time > 540:  # 9시간(540분) 이상
            score += 20
        elif 240 <= time < 420:  # 4시간(240분)부터 7시간(420분) 미만
            score += 15
        elif time < 240:  # 4시간(240분) 미만
            score += 10
        if time < 120:  # 2시간(120분) 미만
            score = 0

        return score

    def calculate_start_sleep_score(time):
        score = 0
               
        if 1200 <= time < 1380:  # 20:00 ~ 22:59
            score += 25
        elif 1380 <= time < 1440:  # 23:00 ~ 23:59
            score += 20
        elif 0 <= time < 60:  # 00:00 ~ 00:59
            score += 15
        elif 60 <= time < 120:  # 01:00 ~ 01:59
            score += 10
        elif 120 <= time < 300:  # 02:00 ~ 04:59
            score += 5

        return score


    def calculate_bad_position_score(time, sleep_time):
        if sleep_time == 0:
            return 0

        score = 0

        if 0.71 <= time / sleep_time <= 1:
            score += 0
        elif 0.51 <= time / sleep_time <= 0.7:
            score += 10
        elif 0.21 <= time / sleep_time <= 0.5:
            score += 20
        elif time / sleep_time <= 0.2:
            score += 25

        return score
    

    def calculate_position_changes_score(position_changes):
        score = 0
        
        if position_changes >= 16:
            score += 5
        elif 11 <= position_changes <= 15:
            score += 10
        elif 6 <= position_changes <= 10:
            score += 20
        else:
            score += 25

        return score

    # def minutes_to_hours(minutes):
    #     if minutes is None:
    #         return 0.0

    #     hours = round(minutes / 60, 1)
    #     return hours

    sleep_minutes_get =  time_to_minutes(sleeptimeget)
    sleep_time_score = calculate_sleep_time_score(sleep_minutes_get)
    start_minutes_get = time_to_minutes(starttimeget)
    start_sleep_time_score = calculate_start_sleep_score(start_minutes_get)
    bad_position_minutes = time_to_minutes(bad_tuple)
    bad_position_score = calculate_bad_position_score( bad_position_minutes, sleep_minutes_get)
    position_change_score = calculate_position_changes_score(position_changes)

    print(sleeptimeget)
    print(sleep_minutes_get)


    # total_sleep_time = minutes_to_hours(sleep_minutes_get)
    # start_sleep_time = minutes_to_hours(start_minutes_get)
    # bad_position_time = minutes_to_hours(bad_position_minutes)
    

    total_sleep_score = (sleep_time_score + start_sleep_time_score + bad_position_score + position_change_score)

    result = {

        "total_sleep_score": total_sleep_score,
        "position_change_score": position_change_score,
        "bad_position_score": bad_position_score,
        "sleep_time_score": sleep_time_score,
        "start_sleep_time_score": start_sleep_time_score,

    }

    print(result)
    return JSONResponse(content=result)