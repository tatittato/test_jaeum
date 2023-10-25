from pydantic import BaseModel
from datetime import date, datetime  # datetime 모듈 임포트


class UserBase(BaseModel):
    nickname: str

class SleepInfoBase(BaseModel):
    nickname: str
    start_sleep: str
    end_sleep: str
    total_sleep: str
    total_sleep_score: int

class SleepEventBase(BaseModel):
    sleep_event_id: int
    sleep_info_id: int
    nickname: str
    sleep_event: str
    event_time: datetime

# class SleepEventDataBase(BaseModel):
#     event_data_id = int
#     sleep_info_id = int
#     sleep_event_id = int
#     nickname = str
#     event_data_path = str