from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from .database import Base, engine

class User(Base):
    __tablename__ = "user"

    nickname = Column(String(10), nullable=False, primary_key=True)


class SleepInfo(Base):
    __tablename__ = "sleep_info"

    sleep_info_id = Column(Integer, autoincrement=True, primary_key=True)
    nickname = Column(String(10), ForeignKey("user.nickname"), nullable=False)
    date = Column(Date)  # Date 데이터 형식으로 날짜 저장
    total_sleep = Column(String(30))  # 총 수면 시간을 문자열로 저장
    start_sleep = Column(String(30))  # 시작 시간을 DateTime 데이터 형식으로 저장
    end_sleep = Column(String(30))  # 종료 시간을 DateTime 데이터 형식으로 저장
    total_sleep_score = Column(Integer) # 수면점수

    # User 테이블과의 관계 설정
    user = relationship("User", backref="sleep_info")


class SleepEvent(Base):
    __tablename__ = "sleep_event"

    sleep_event_id = Column(Integer, autoincrement=True, primary_key=True)
    sleep_info_id = Column(Integer, ForeignKey("sleep_info.sleep_info_id"), nullable=False)
    nickname = Column(String(10), ForeignKey("user.nickname"), nullable=False)
    sleep_event = Column(String(10), nullable=True)
    event_time = Column(DateTime)  # DateTime 데이터 형식으로 날짜 및 시간 저장

    # User 테이블과 SleepInfo 테이블과의 관계 설정
    user = relationship("User", backref="sleep_event")
    sleep_info = relationship("SleepInfo", backref="sleep_event")


class SleepEventData(Base):
    __tablename__ = "sleep_event_data"

    event_data_id = Column(Integer, autoincrement=True, primary_key=True)
    sleep_info_id = Column(Integer, ForeignKey("sleep_info.sleep_info_id"), nullable=False)
    sleep_event_id = Column(Integer, ForeignKey("sleep_event.sleep_event_id"), nullable=False)
    nickname = Column(String(10), ForeignKey("user.nickname"), nullable=False)
    event_data_path = Column(String(30))

    # User 테이블과 SleepInfo, SleepEvent 테이블과의 관계 설정
    user = relationship("User", backref="sleep_event_data")
    sleep_info = relationship("SleepInfo", backref="sleep_event_data")
    sleep_event = relationship("SleepEvent", backref="sleep_event_data")

# 처음 한번만 생성
Base.metadata.create_all(engine)