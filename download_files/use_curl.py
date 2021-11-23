import os

exe = 'curl ' #curl 문

if os.system(exe) == 0:     #정상종료시 0
    print('download success')
else:
    print('not downloaded')


