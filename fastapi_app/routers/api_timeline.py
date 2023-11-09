from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.orm import Session

from ..database import SessionLocal, engine
from ..model import *


from datetime import datetime

router = APIRouter(
    tags=["Timeline"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SleepInfoBase(BaseModel):
    nickname: str
    date: str
    total_sleep: str
    start_sleep: str
    end_sleep: str


class SleepEventBase(BaseModel):
    sleep_event: str
    event_time: str
    event_data_path: str


class SleepTimelineResponse(BaseModel):
    sleep_info: List[SleepInfoBase]
    sleep_events: Optional[List[SleepEventBase]]


@router.get("/timeline/search", response_model=SleepTimelineResponse)
async def fetch_timeline_data(date: str, nickname: str, db: Session = Depends(get_db)):
    if not date:
        raise HTTPException(status_code=400, detail="Date parameter is required.")

    target_date = datetime.strptime(date, "%Y-%m-%d").date()

    # `SleepInfo`에서 `date`와 `nickname`을 만족하는 데이터만 필터링
    sleep_info_entries = (
        db.query(SleepInfo)
        .filter(SleepInfo.date == target_date, SleepInfo.nickname == nickname)
        .all()
    )

    sleep_info_data = [
        {
            "nickname": item.nickname,
            "date": item.date.strftime("%Y-%m-%d"),
            "total_sleep": item.total_sleep,
            "start_sleep": item.start_sleep,
            "end_sleep": item.end_sleep,
        }
        for item in sleep_info_entries
    ]

    # `SleepEvent`와 `SleepInfo`를 조인하여 두 조건을 만족하는 데이터만 필터링
    sleep_event_entries = (
        db.query(SleepEvent)
        .join(SleepInfo, SleepEvent.sleep_info_id == SleepInfo.sleep_info_id)
        .filter(SleepInfo.nickname == nickname, SleepInfo.date == target_date)
        .all()
    )

    sleep_event_data = [
        {
            "sleep_event": item.sleep_event,
            "event_time": item.event_time,
            "event_data_path": "/static/images/pose/" + item.event_data_path,
        }
        for item in sleep_event_entries
    ]

    print(sleep_event_data)

    return {"sleep_info": sleep_info_data, "sleep_events": sleep_event_data}
