from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..model import *

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


@router.get("/timeline", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    sleep_event_data = (
        db.query(SleepEvent)
        .filter(SleepEvent.sleep_info_id == SleepInfo.sleep_info_id)
        .all()
    )

    print("DB연동 확인")
    print(sleep_event_data)

    return templates.TemplateResponse(
        "timeline.html", {"request": request, "sleep_event_data": sleep_event_data}
    )
