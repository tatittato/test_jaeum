from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    "root", "12341234", "127.0.0.1", 3306, "jaeum"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 엔진생성
engine = create_engine(DATABASE_URL)

# 세션생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base 객체생성
Base = declarative_base()

# 데이터베이스 연결을 시도하고 간단한 쿼리를 실행합니다.
try:
    # 세션 생성
    Session = sessionmaker(bind=engine)
    session = Session()

    # 간단한 쿼리 실행, 예를 들어 현재 타임스탬프를 선택합니다.
    result = session.execute(text("SELECT NOW()"))
    current_time = result.scalar()

    print("데이터베이스 연결이 성공했습니다. 현재 시간:", current_time)

except Exception as e:
    print("데이터베이스 연결에 실패했습니다. 오류:", e)

finally:
    # 세션을 닫습니다.
    session.close()
