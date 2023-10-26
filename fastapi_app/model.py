from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime,text
from sqlalchemy.orm import relationship
from .database import Base, engine
from sqlalchemy.sql import func

# User 테이블
class User(Base):
    __tablename__ = "user"

    nickname = Column(String(255), nullable=False, primary_key=True)


# 수면 정보 테이블
class SleepInfo(Base):
    __tablename__ = "sleep_info"

    sleep_info_id = Column(Integer, autoincrement=True, primary_key=True)
    nickname = Column(String(255), ForeignKey("user.nickname"), nullable=False)
    date = Column(Date, default=func.now())   
    total_sleep = Column(String(255))  
    start_sleep = Column(String(255)) 
    end_sleep = Column(String(255))  
    total_sleep_score = Column(Integer)
    sleep_time_score = Column(Integer)
    start_sleep_time_score = Column(Integer)
    bad_position_score = Column(Integer)
    position_change_score = Column(Integer) 

# 수면 이벤트 테이블
class SleepEvent(Base):
    __tablename__ = "sleep_event"

    sleep_event_id = Column(Integer, autoincrement=True, primary_key=True)
    sleep_info_id = Column(Integer, ForeignKey("sleep_info.sleep_info_id"), nullable=False)
    sleep_event = Column(String(255), nullable=True)
    event_time = Column(String(255)) 
    event_data_path = Column(String(255))



# 처음 한번만 생성
Base.metadata.create_all(engine)