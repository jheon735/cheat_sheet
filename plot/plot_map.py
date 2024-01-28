import matplotlib.pyplot as plt
from pyproj import CRS, Transformer, Proj
import shapefile
import numpy as np

def draw_object(title):
    #사용하려는 shpae파일의 정보를 기록. 아래 정보는 기상청 shape파일
    GridProj = 'lcc'
    GridCenterLat = 38.0
    GridCenterLon = 126.0
    Lat1 = 30.
    Lat2 = 60.

    GridCenterX = 1121  #지도위에 그릴 그리드 정보
    GridCenterY = 1681
    GridResol = 500

    projectionstr = f'+proj={GridProj} +lat_0={GridCenterLat} +lon_0={GridCenterLon} +lat_1={Lat1} +lat_2={Lat2} unit=m'
    lcc_proj = Proj(projectionstr)
    wgs84 = CRS("epsg:4326")
    lonlat2xy = Transformer.from_proj(wgs84, lcc_proj)

    fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))

    # MAP Drawing
    shpfile = 'shapefile.shp'  #shape파일 입력
    sf = shapefile.Reader(shpfile)  # , encoding=shpencode)
    add = 0
    for shape in sf.shapeRecords():
        parts = shape.shape.parts
        npoly = len(parts)
        shpx, shpy = [i[0] for i in shape.shape.points[:]], [i[1] for i in shape.shape.points[:]]
        parts.append(len(shpx))
        rec = sf.record(add)

        if rec[4] == 'South Korea' or rec[4] == 'North Korea' or rec[4] == 'Japan' \
                or rec[4] == 'China' or rec[4] == 'Russia':  # add != 9999999 :
            for k in range(0, npoly):
                part_x = shpx[parts[k]:parts[k + 1]]
                part_y = shpy[parts[k]:parts[k + 1]]
                part_xx, part_yy = lonlat2xy.transform(part_y, part_x)
                part_xx = np.array(part_xx) / GridResol + GridCenterX
                part_yy = np.array(part_yy) / GridResol + GridCenterY
                ax1.plot(part_xx, part_yy, color='gray', linewidth=0.3)

        add = add + 1

    ax1.set_xlim([200, 2305])
    ax1.set_ylim([100, 2300])
    ax1.set_aspect('equal', 'box')
    ax1.set_xticklabels([])
    ax1.set_xticks([])
    ax1.set_yticklabels([])
    ax1.set_yticks([])

    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.close()