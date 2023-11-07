from pydantic import BaseModel, Field
from typing import List, Optional




class UserBase(BaseModel):
    nickname: str

class SleepInfoCreate(BaseModel):
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

class SleepInfoFeedbackUpdate(BaseModel):
    sleep_feedback: str  

class SleepInfoIdGet(BaseModel):
    nickname: str

# Pydantic 모델을 사용하여 요청의 body에서 데이터를 추출
class RequestData(BaseModel):
    nickname: str
    sleep_info_id: int

class SleepInfoGet(BaseModel):
    total_sleep: str
    start_sleep: str
    end_sleep: str
    sleep_event: List[str] = []
    event_time: List[str] = []

class SleepInfoFeedback(BaseModel):
    sleep_feedback : str

class SleepEventBase(BaseModel):
    sleep_info_id: int
    sleep_event: str
    event_time: str
    event_data_path: str

class SleepInfoBase(BaseModel):
    nickname: str
    date: str
    total_sleep: str
    start_sleep: str
    end_sleep: str

class SleepTimelineResponse(BaseModel):
    sleep_info: List[SleepInfoBase]
    sleep_events: Optional[List[SleepEventBase]]
    


