from ftplib import FTP
from datetime import datetime
from dateutil import parser

with FTP("ip") as ftp:
    ftp.login("id", "pw")
    ftp.set_pasv(False) #passive mode 설정
    ftp.cwd("path")
    files = ftp.nlst()  #파일 목록

    mod_time = ftp.voidcmd('MDTM ' + "fname")[4:]   #수정 시간
    mt = datetime.strptime(mod_time, '%Y%m%d%H%M%S')
    fsize = ftp.size("fname") #파일 크기

    dirs = []       #dir로 상세 정보 포함 파일 목록 확인하여 파일 정보 얻는 법
    ftp.dir("fname", dirs.append)
    dirs = dirs[0]
    tokens = dirs.split(maxsplit=9)
    time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
    size = tokens[4]
    ftp_mtime = parser.parse(time_str)


    with open("save fname", 'wb') as f:
        ftp.retrbinary('RETR ' + "fname", f.write)

    lines = []
    ftp.retrlines('RETR ' + "fname", lines.append)