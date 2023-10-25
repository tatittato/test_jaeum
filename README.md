## Installation

1. install python3.10

2. install packages

```bash
# You can add package names to this requirements.txt
pip install -r requirements.txt
```

## execute web server

```bash
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

## connect to web server

http://127.0.0.1:8000

## connect api document

http://127.0.0.1:8000/docs

## file structure

```
.
├── fastapi_app
│   ├── routers # api routers
│   |   ├── statistics_crud.py # 수면통계 crud 함수 모듈
│   ├── routers # api routers
│   |   ├── api_record.py # 수면측정 관련 api 구현 파일
│   |   ├── api_score.py # 수면점수 관련 api 구현 파일
│   |   ├── api_statistics.py # 수면통계 관련 api 구현 파일
│   |   ├── api_timeline.py # 수면타임라인 관련 api 구현 파일
│   ├── utils
│   |   ├── light
│   |   |   ├── increase_brightness.py # 밝기 조절 모듈
│   |   |   ├── increase_contrast.py # 대비 조절 모듈
│   |   |   ├── mesure_brigtness.py # 밝기 측정 모듈
│   |   ├── pose_recognize
│   |   |   ├── calculate_angle.py # 랜드마크 각도 계산 모듈
│   |   |   ├── classify_pose.py # 자세 구분 모듈
│   |   |   ├── detect_pose.py # 자세 감지 모듈
│   |   |   ├── pose.py # 자세 지정 모듈
│   |   ├── statistics_functions.py # 수면통계 관련 함수 모듈
│   ├── views
│   |   ├── record.py # 수면측정 웹페이지 구현 파일
│   |   ├── score.py # 수면점수 웹페이지 구현 파일
│   |   ├── statistics.py # 수면통계 웹페이지 구현 파일
│   |   ├── ranking.py # 수면타임라인 웹페이지 구현 파일
│   ├── main.py # main file of fastapi. uwsgi will run this file to start web server.
├── static # static files, you can access files in this directory by http://127.0.0.1:8000/static/css/home.css
│   ├── background # background image
│   ├── css # css files
│   ├── img # image files
│   └── js # javascript files
├── templates # html files
│   ├── record.html # 수면측정 웹페이지
│   ├── score.html # 수면점수 웹페이지
│   ├── statistics.html # 수면통계 웹페이지
│   ├── timeline.html # 수면타임라인 웹페이지
├── README.md # this file
├── requirements.txt # python package list
```
