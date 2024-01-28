import numpy as np
from matplotlib import colors

def make_cmap():
    cc = np.loadtxt(f'colortable_example.txt')  # 구간별 색 rgb값으로 colortalbe만들기
    cmaplist = []
    for i in cc:
        cmaplist.append(tuple(np.append(i[:3] / 255, 1)))

    cmap = colors.LinearSegmentedColormap.from_list(
        'custom', cmaplist, len(cmaplist)
    )
    bounds = np.append(-99, cc[:, -1])
    norm = colors.BoundaryNorm(bounds, len(cmaplist))
    return cmap, norm