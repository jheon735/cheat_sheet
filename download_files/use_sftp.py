import pysftp
from datetime import datetime

with pysftp.Connection("ip", username="id", password="pw") as sftp:
    with sftp.cd("remote"):
        info = sftp.stat("fname")   #파일 정보 볼 수 있는 여러 info 정보
        mt = datetime.utcfromtimestamp(info.st_mtime)   #파일 수정 시간

        sftp.get("fname", localpath="local / fname")

