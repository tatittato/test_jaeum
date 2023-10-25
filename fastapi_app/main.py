from fastapi.staticfiles import StaticFiles


from fastapi import FastAPI, Depends

from .database import SessionLocal, engine

# from .crud import *
# from .schemas import *
# from .model import *
# from sqlalchemy.orm import Session

from .routers import api_record, api_score, api_statistics, api_timeline

from .views import home, record, score, statistics, timeline

tags_metadata = [
    {
        "name": "Record",
        "description": "수면 측정 관련 API",
    },
    {
        "name": "Score",
        "description": "수면점수 관련 API",
    },
    {
        "name": "Statistics",
        "description": "수면 통계정보 관련 API",
    },
    {
        "name": "Timeline",
        "description": "수면 타임라인 관련 API",
    },
    {
        "name": "Web Pages",
        "description": "웹 페이지 (API 아님)",
    }
]
app = FastAPI(openapi_tags=tags_metadata, title="api", version="0.0.1", )

# routers = [home, ranking, rank, speech]
routers = [home, record, score, statistics, timeline, api_record, api_score, api_statistics, api_timeline]
for r in routers:
    app.include_router(r.router)

app.mount("/static", StaticFiles(directory="static"), name="static")






