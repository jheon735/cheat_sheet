from pymap3d import ecef, eci
from datetime import datetime

lat = 35.91     #위도
lon = 127.77    #경도

x, y, z=ecef.geodetic2ecef(lat, lon, 0)   #위도, 경도, 고도(geodetic ellipsoid 기준, 0일때 지표면) geodetic 좌표계를 ecef로 만들어줌. x, y, z로 output

t = datetime(2021, 3, 5, 0,0,0)
nx, ny, nz = eci.ecef2eci(x, y, z, t)   #ecef 좌표를 eci 좌표로
