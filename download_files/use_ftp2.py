from ftplib import FTP_TLS as FTP2
from dateutil import parser
from datetime import datetime, timedelta

with FTP2("ip") as ftp:
    ftp.login()
    ftp.cwd("path")  # 경로로 이동
    cdir = []
    ftp.dir("fname", cdir.append)  # 파일 목록 자세히와 같은 목록 얻을 수 있음

    cdir = cdir[0].split()

    fname = cdir[-1]
    tinfo = ' '.join(cdir[5:8]) #파일 수정 시간
    ftp_mtime = parser.parse(tinfo)
    ftp_size = int(cdir[4]) #파일 크기

    dirs = cdir[0]      #dir로 상세 정보 포함 파일 목록 확인하여 파일 정보 얻는 법
    tokens = dirs.split(maxsplit=9)
    time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
    size = tokens[4]
    ftp_mtime = parser.parse(time_str)

    with open("save fname", 'wb') as f:
        ftp.retrbinary('RETR ' + fname, f.write)
