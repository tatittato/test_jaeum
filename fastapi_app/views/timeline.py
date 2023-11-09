from fastapi import APIRouter
from fastapi import Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date

from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..model import *
from ..schemas import *

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


@router.get("/timeline", response_class=HTMLResponse)
async def home_page(
    request: Request, db: Session = Depends(get_db), nickname: str = Query(None)
):
    today = date.today()

    # URL에서 가져온 닉네임과 DB의 User 테이블에서 닉네임을 비교하여 필터링합니다.
    if nickname:
        user = db.query(User).filter(User.nickname == nickname).first()
        if user:
            user_id = user.nickname
            sleep_event_data = (
                db.query(SleepEvent)
                .join(SleepInfo, SleepEvent.sleep_info_id == SleepInfo.sleep_info_id)
                .filter(SleepInfo.date == today, SleepInfo.nickname == user_id)
                .all()
            )
        else:
            sleep_event_data = []  # 사용자가 존재하지 않으면 데이터를 빈 리스트로 초기화
    else:
        sleep_event_data = []  # 닉네임이 URL에 제공되지 않으면 데이터를 빈 리스트로 초기화

    return templates.TemplateResponse(
        "timeline.html", {"request": request, "sleep_event_data": sleep_event_data}
    )