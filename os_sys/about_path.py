import sys
import os
import shutil
from pathlib import Path

pathjoin=os.sep.join(["path1", "path2"])    #하위경로 추가

if not os.path.isdir("path"):       #디렉토리 존재 여부 확인
    os.makedirs("path")     #디렉토리 생성

if os.path.isfile("path"):      #파일 존재 여부 확인
    print("file already exist")

os.remove("path")   #파일 삭제

os.path.abspath("path")     #상대 경로를 입력하면 절대 경로를 알려줌

os.path.dirname(os.path.abspath((os.path.dirname(__file__))))   #현재 파일의 디렉토리

shutil.rmtree("path")   #지정해준 path이하 tree전부 삭제

local_dir = Path("D:/test/hi")  #변수를 문자열이 아닌 경로로 인식하여 경로 다룰 때 사용하기 편해짐
new_dir = local_dir / "someting" #Path로 지정한 후에는 다음과 같은 형태로 사용가능
