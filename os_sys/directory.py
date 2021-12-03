import sys
import os
import shutil

pathjoin=os.sep.join(["path1", "path2"])    #하위경로 추가

if not os.path.isdir("path"):       #디렉토리 존재 여부 확인
    os.makedirs("path")     #디렉토리 생성

if os.path.isfile("path"):      #파일 존재 여부 확인
    print("file already exist")

shutil.rmtree("path")   #지정해준 path이하 tree전부 삭제

