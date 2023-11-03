from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Union, Tuple
from ..models import statistics_crud
from ..database import get_db
from ..schemas import SleepInfoBase, SleepEventBase
from sqlalchemy.orm import Session
import numpy as np
from ..utils import statistics_functions

router = APIRouter(
    tags=["Statistics"],
    responses={404: {"description": "Not found"}},
)

chart_label = []
start_day = None

# 리턴타입힌트 정리용 변수처리
period_return_hint = Dict[str, Union[Dict[str, int], Tuple[int, int, int]]]

# ▼▼▼▼▼▼ 기간별 평균 수면시간 ▼▼▼▼▼▼
@router.get("/statistics/{nickname}/{period}") #경로 매개변수 사용
async def get_period_data(period: str, nickname: str, db: Session = Depends(get_db)) -> Dict[str, Union[int, float, str, Tuple[int, int, int], List[str], List[int], period_return_hint]]:
    period_average =[]
    global chart_label
    global start_day
    
    # 7일간 수면현황 + 기간별 수면현황(1주) 에서 사용할 start_day 변수 설정.
    end_day = statistics_functions.decide_start_day_by_period(period)
    
    # db 데이터 가져오기
    period_data = statistics_crud.get_sleep_data(db=db, start=start_day, end=end_day, nickname=nickname, response_model=SleepInfoBase)

    if period_data:
        period_first_last = statistics_functions.get_first_last_day(period_data)
        dataframe_datas = statistics_functions.to_dataframe_period(period_data)
        score_average = dataframe_datas.iloc[0]['score_average']

        if period != 'week':
            dataframe_datas  = statistics_functions.get_data_period(dataframe_datas, period)

        dict_datas, period_average, period_total = statistics_functions.divide_dataframe_process_period(dataframe_datas, period)
    else:
        period_first_last = ["-", "-"]
        dict_datas = "-"
        score_average = 0
        period_total = 0
        period_average = 0
        
    return {"chart_data": dict_datas, "score_average": score_average, "period_first_last":period_first_last, "period_total":period_total, "period_average":period_average}


# ▼▼▼▼▼▼ 자세별 발생 횟수 ▼▼▼▼▼▼
@router.get("/statistics/{nickname}/{period}/{pose}")
async def get_chart_pose(period: str, pose: str, nickname: str, db: Session = Depends(get_db)) -> Dict[str, Union[int, str, Dict[str, Dict[str, int]]]]:

    if period == "entire":
        event_data = statistics_crud.get_sleep_event_data(start=None, end=end_day, nickname = nickname, db=db, response_model=SleepInfoBase)
    else:
        event_data = statistics_crud.get_sleep_event_data(start=start_day, end=end_day, nickname = nickname, db=db, response_model=SleepEventBase)

    if event_data is None or len(event_data) == 0:
        dict_datas = "-"
        return {"chart_data": dict_datas}
    else: 
        try:
            dataframe_datas = statistics_functions.to_dataframe_pose(event_data)
            dataframe_datas = statistics_functions.get_data_period(dataframe_datas, period)
            dict_datas = statistics_functions.trans_date_dataframte_pose(dataframe_datas)
        except Exception as e:
            dict_datas = "-"
            return {"chart_data": dict_datas}       
        
        return {"chart_data": dict_datas }


