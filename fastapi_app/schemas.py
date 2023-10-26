from pydantic import BaseModel
from typing import ClassVar



class UserBase(BaseModel):
    nickname: str

class SleepInfoBase(BaseModel):
    nickname: str
    start_sleep: str

class SleepInfoUpdate(BaseModel):
    end_sleep: str
    total_sleep: str

class SleepInfoScoreUpdate(BaseModel):
    total_sleep_score : int
    sleep_time_score : int
    start_sleep_time_score : int
    bad_position_score : int
    position_change_score : int     

class SleepInfoIdGet(BaseModel):
    nickname: str

class SleepEventBase(BaseModel):
    sleep_info_id: int
    sleep_event: str
    event_time: str
    event_data_path: str



