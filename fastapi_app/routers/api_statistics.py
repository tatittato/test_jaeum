from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Union, Tuple
from ..models import statistics_crud
from ..database import get_db
from ..schemas import SleepInfoBase, SleepEventBase
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from ..utils import statistics_functions

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Statistics"],
    responses={404: {"description": "Not found"}},
)

# 시간데이터는 모두 초로 환산하여 계산 후 front단에서 다시 시간으로 변환하여 출력
# 시간형식 str 문자열을 초로 환산
def time_str_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return int(np.array([hours * 3600 + minutes * 60 + seconds]))

chart_label = []
start_day = None
today = date.today()
end_day = today

# 리턴타입힌트 정리용 변수처리
period_return_hint = Dict[str, Union[Dict[str, int], Tuple[int, int, int]]]

# ▼▼▼▼▼▼ 기간별 평균 수면시간 ▼▼▼▼▼▼
@router.get("/statistics/{period}/") #경로 매개변수 사용
async def get_period_data(period: str, db: Session = Depends(get_db)) -> Dict[str, Union[int, float, Tuple[int, int, int], List[str], List[int], period_return_hint]]:
    # today = date.today()
    # end_day = today
    period_average =[]
    global chart_label
    global start_day

    # 7일간 수면현황 + 기간별 수면현황(1주) 에서 사용할 start_day 변수 설정.
    if period == "week":
        print(period)
        # 조회 당일을 기준(end_parameter) 6일전(start_parameter)
        start_day = end_day - timedelta(days=6)
    elif period == "month":
        # 조회 당월을 기준(end_parameter) 당월 데이터만!
        start_day = date(today.year, end_day.month, 1)
    elif period == "sixmonths":
        # 조회 당월을 기준, 5개월 전까지 (총 6개월)
        start_day = end_day - relativedelta(months=5)
        start_day = date(start_day.year, start_day.month, 1)
    elif period == "year":
        # 조회 연도를 기준 당 해 분량의 평균 수면시간을 계산하여 반환
        start_day = date(end_day.year, 1, 1)
    elif period == "entire":
        # 오늘 ~ 이전 전체 기간동안의 데이터
        start_day = None
    else:
        return {"error": "Invalid period specified"}
    
    period_data = statistics_crud.get_sleep_data(db=db, start=start_day, end=end_day, response_model=SleepInfoBase)

    if period_data:
        period_first_last = statistics_functions.get_first_last_day(period_data)
        dataframe_datas = statistics_functions.to_dataframe_period(period_data)
        print("="*60)
        print("dataframe화 한 get_데이터")
        print(dataframe_datas)
        print("score_average")
        score_average = dataframe_datas.iloc[0]['score_average']
        print("score_average 점수는요? ", type(score_average), str(score_average))
        print(dataframe_datas.iloc[0]['score_average'])
        print("="*60)

        if period != 'week':
            dataframe_datas  = statistics_functions.get_data_period(dataframe_datas, period)
            print(type(dataframe_datas))
            print(dataframe_datas)
        dict_datas, period_average, period_total = statistics_functions.divide_dataframe_process_period(dataframe_datas, period)
        print(type(dict_datas))
        print(dict_datas)
    else:
        dict_datas = np.zeros(5).tolist()
        period_total = 0
        period_average = 0
        
    return {"chart_data": dict_datas, "score_average": score_average, "period_first_last":period_first_last, "period_total":period_total, "period_average":period_average}


# ▼▼▼▼▼▼ 자세별 발생 횟수 ▼▼▼▼▼▼
@router.get("/statistics/{period}/{pose}")
async def get_chart_pose(period:str, pose: str, db: Session = Depends(get_db)) -> Dict[str, Dict[str, Dict[str, int]]]:
    if period == "entire":
        event_data = statistics_crud.get_sleep_event_data(start=None, end=end_day, db=db, response_model=SleepInfoBase)
    else:
        event_data = statistics_crud.get_sleep_event_data(start=start_day, end=end_day, db=db, response_model=SleepEventBase)

    if event_data is None or len(event_data) == 0:
        dict_datas = np.zeros(5).tolist()
        return {"chart_data": dict_datas}
    else: 
        # 여기서 자세별로 구현해야된다
        try:
            dataframe_datas = statistics_functions.to_dataframe_pose(event_data)
            # data를 나눌 범위설정
            dataframe_datas = statistics_functions.get_data_period(dataframe_datas, period)
            dict_datas = statistics_functions.trans_date_dataframte_pose(dataframe_datas)

        except Exception as e:
            print("Exception")
            print(e)
            dict_datas = np.zeros(5).tolist()
            return {"chart_data": dict_datas}
        
        return {"chart_data": dict_datas }


