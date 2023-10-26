from pydantic import BaseModel
from typing import ClassVar
from typing import List, Optional


class UserBase(BaseModel):
    nickname: str


class SleepInfoUpdate(BaseModel):
    end_sleep: str
    total_sleep: str


class SleepInfoIdGet(BaseModel):
    nickname: str


class SleepInfoBase(BaseModel):
    nickname: str
    date: str
    total_sleep: str
    start_sleep: str
    end_sleep: str


class SleepEventBase(BaseModel):
    sleep_info_id: int
    sleep_event: str
    event_time: str
    event_data_path: str


class SleepTimelineResponse(BaseModel):
    sleep_info: List[SleepInfoBase]
    sleep_events: Optional[List[SleepEventBase]]
