from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    DateTime,
    text,
)
from sqlalchemy.orm import relationship
from .database import Base, engine
from sqlalchemy.sql import func


# User 테이블
class User(Base):
    __tablename__ = "user"

    nickname = Column(String(10), nullable=False, primary_key=True)


# 수면 정보 테이블
class SleepInfo(Base):
    __tablename__ = "sleep_info"

    sleep_info_id = Column(Integer, autoincrement=True, primary_key=True)
    nickname = Column(String(10), ForeignKey("user.nickname"), nullable=False)
    date = Column(Date, default=func.now())
    total_sleep = Column(String(30))
    start_sleep = Column(String(30))
    end_sleep = Column(String(30))

    sleep_events = relationship("SleepEvent", back_populates="sleep_info")


# 수면 이벤트 테이블
class SleepEvent(Base):
    __tablename__ = "sleep_event"

    sleep_event_id = Column(Integer, autoincrement=True, primary_key=True)
    sleep_info_id = Column(
        Integer, ForeignKey("sleep_info.sleep_info_id"), nullable=False
    )
    sleep_event = Column(String(10), nullable=True)
    event_time = Column(String(30))
    event_data_path = Column(String(50))

    sleep_info = relationship("SleepInfo", back_populates="sleep_events")


# 처음 한번만 생성
Base.metadata.create_all(engine)
