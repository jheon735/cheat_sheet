from datetime import datetime, timedelta

tt = datetime.utcnow()  #utc 시간 받아오기

tt = datetime(2019, 3, 6, 14, 53, 45)   #시간 입력

idate='201903061453'
tt = datetime.strptime(idate, '%Y%m%d%H%M') #string에서 datetime 정보 입력

stdtime=tt.strftime('%Y%m%d')   #datetime을 string으로 뽑아내기 https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
ymd=tt.strftime('%Y-%m-%d')     #다른 예시

ynt=tt-timedelta(days=1)    #시간 계산
