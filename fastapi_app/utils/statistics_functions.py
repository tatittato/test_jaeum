import pandas as pd
import numpy as np
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

def time_str_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return int(np.array([hours * 3600 + minutes * 60 + seconds]))

today = date.today()
end_day = today

def decide_start_day_by_period(period):
  end_day = today
  if period == "week": # 조회 당일을 기준(end_parameter) 6일전(start_parameter)
      start_day = end_day - timedelta(days=6)
  elif period == "month": # 조회 당월을 기준(end_parameter) 당월 데이터만!
      start_day = date(today.year, end_day.month, 1)
  elif period == "sixmonths": # 조회 당월을 기준, 5개월 전까지 (총 6개월)
      start_day = end_day - relativedelta(months=5)
      start_day = date(start_day.year, start_day.month, 1)
  elif period == "year": # 조회 연도를 기준 당 해 분량의 평균 수면시간을 계산하여 반환
      start_day = date(end_day.year, 1, 1)
  elif period == "entire": # 오늘 ~ 이전 전체 기간동안의 데이터
      start_day = None
  else:
      return {"error": "Invalid period specified"}  
  return start_day

# ▼▼▼▼▼ 기간으로 나누는 부분 시작 ▼▼▼▼▼
def get_first_last_day(period_data):
  first_day = period_data[0]['date'].strftime('%y/%m/%d')
  last_day = period_data[-1]['date'].strftime('%y/%m/%d')
  period_first_last = [first_day, last_day]
  return period_first_last

# db에서 가져온 dataFrrame을 DataFrame화 하여 반환
def to_dataframe_period(period_data):
  df = pd.DataFrame(period_data)
  df['date'] = pd.to_datetime(df['date'])
  # str 시간데이터를 초로 환산한 뒤 df에 다시 저장
  df['total_seconds'] = df['total_sleep'].apply(time_str_to_seconds)
  df['start_sleep'] = df['start_sleep'].apply(time_str_to_seconds)
  df['end_sleep'] = df['end_sleep'].apply(time_str_to_seconds)
  # df['score_average'] = df['total_sleep_score'].mean().astype(float)
  df['score_average'] = round(df['total_sleep_score'].mean(), 1)
  return df

# 기간 범위를 설정해서 그룹화할 준비
def get_data_period(df, period):
  if period == "week":
    df['tag'] = df['date'].dt.strftime('%y/%m/%d')

  elif period == "month":
    df['fotmatted_date'] = df['date'].dt.strftime('%d')
    df['fotmatted_date'] = df['fotmatted_date'].astype(int)
    bins = [0, 7, 14, 21, 28, float('inf')]
    labels = [f"{i}주차" for i in range(1, 6)]
    df['tag'] = pd.cut(df['fotmatted_date'], bins=bins, labels=labels, right=True)

  elif period == "sixmonths":
    df['tag'] = df['date'].dt.strftime('%y/%m')

  elif period == "year" or period == "entire":
    df['tag'] = df['date'].dt.strftime('%Y')

  return df

# 기간별로 데이터를 정제해서 내보냄 (뿌려줄 dict_datas, 평균값, 총합)
def divide_dataframe_process_period(df, period):
  dict_datas = {}
  period_average = 0
  period_total = 0

  if period == "week":
    period_total = int(df['total_seconds'].sum())
    period_average = int(df['total_seconds'].mean())
    dict_datas = dict(zip((df['date'].dt.strftime('%y/%m/%d')), zip(df['start_sleep'], df['end_sleep'], df['total_seconds'])))
  
  else : 
    period_total = df.groupby('tag', observed=False)['total_seconds'].sum().to_list()
    period_average = df.groupby('tag', observed=False)['total_seconds'].mean().fillna(0).astype(int).to_list()
    tags = df['tag'].unique()
    for idx, tag in enumerate(tags):
      key_name = f"{tag}"
      dict_datas[key_name] = {'total': period_total[idx], 'average': period_average[idx]}

  # 평균점수, 총합을 재설정해서 반환한다
  period_average = int(df['total_seconds'].mean())
  period_total = int(df['total_seconds'].sum())
  return dict_datas, period_average, period_total


# ▼▼▼▼▼ 자세별로 나누는 부분 시작 ▼▼▼▼▼
# 받아온 데이터를 dataFrame화한다
def to_dataframe_pose(event_data):
  df = pd.DataFrame(event_data)
  df['date'] = pd.to_datetime(df['date'])
  return df

# 슬립이벤트를 잘라서 저장해놓는 준비를 한다
def trans_date_dataframte_pose(df):
  # 1. 각 `sleep_event`의 문자열을 분할
  s = df['sleep_event'].str.split(expand=True).stack()
  idx = s.index.get_level_values(0)
  df_expanded = df.loc[idx].copy()
  df_expanded['word'] = s.values

  # 2. 집계 수행
  result_df = df_expanded.groupby(['tag', 'word'], observed=False).size().unstack(fill_value=0)
  print('result_df')
  print(result_df)
  result_dict = result_df.to_dict(orient='index')
  return result_dict


