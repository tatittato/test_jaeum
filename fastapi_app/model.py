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

    # User 테이블과의 관계 설정
    # user = relationship("User", backref="sleep_info")
# 수면 이벤트 테이블
class SleepEvent(Base):
    __tablename__ = "sleep_event"

    sleep_event_id = Column(Integer, autoincrement=True, primary_key=True)
    sleep_info_id = Column(Integer, ForeignKey("sleep_info.sleep_info_id"), nullable=False)
    sleep_event = Column(String(255), nullable=True)
    event_time = Column(String(255)) 
    event_data_path = Column(String(255))

    # # User 테이블과 SleepInfo 테이블과의 관계 설정
    # sleep_info = relationship("SleepInfo", backref="sleep_event")

# class SleepEventData(Base):
#     __tablename__ = "sleep_event_data"

#     event_data_id = Column(Integer, autoincrement=True, primary_key=True)
#     sleep_info_id = Column(Integer, ForeignKey("sleep_info.sleep_info_id"), nullable=False)
#     sleep_event_id = Column(Integer, ForeignKey("sleep_event.sleep_event_id"), nullable=False)
#     nickname = Column(String(10), ForeignKey("user.nickname"), nullable=False)
#     event_data_path = Column(String(30))

#     # User 테이블과 SleepInfo, SleepEvent 테이블과의 관계 설정
#     user = relationship("User", backref="sleep_event_data")
#     sleep_info = relationship("SleepInfo", backref="sleep_event_data")
#     sleep_event = relationship("SleepEvent", backref="sleep_event_data")

# 처음 한번만 생성
Base.metadata.create_all(engine)