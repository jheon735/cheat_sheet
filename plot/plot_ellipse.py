import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.patches as mpatches
from math import pi, cos, sin

def ellipse_pnt(e_info):
    x = e_info[0]
    y = e_info[1]
    rm = e_info[2]
    rn = e_info[3]
    angle = e_info[4]
    t = np.linspace(0, 2 * pi, 100)
    ell = np.array([rm * np.cos(t), rn * np.sin(t)])
    r_rot = np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])

    ell_rot = np.zeros((2, ell.shape[1]))
    for i in range(ell.shape[1]):
        ell_rot[:, i] = np.dot(r_rot, ell[:, i]) + [x, y]

    return ell_rot


def read_storm_info_ellipse(file):
    f = open(file, 'r')
    lines = f.readlines()

    ellipse = []
    for i in range(5, len(lines)):
        line = lines[i]
        if line[0] == '-': continue
        newLine = ' '.join(line.split())
        data = newLine.split(' ')
        edata = [data[2], data[3], data[6], data[7], data[10], data[-1]]
        if float(data[-1]) == -99: continue
        edata = [float(i) for i in edata]
        ellipse.append(edata)
    f.close()

    return ellipse


def draw_object(title):
    fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))

    oclass = ['CC', 'MCC', 'SLD', 'SLP']
    colors = ['orange', 'green', 'blue', 'red']

    ellipses = []   #x, y, major axis, minor axis, angle 형태의 타원 정보 리스트
    # print(ellipses)
    handle = {}
    for j in range(0, len(ellipses)):
        one_ellip = ellipses[j]
        one_ellip[0], one_ellip[1] = lonlat2xy.transform(one_ellip[1], one_ellip[0])
        one_ellip[0] = one_ellip[0] / GridResol + GridCenterX
        one_ellip[1] = one_ellip[1] / GridResol + GridCenterY
        one_ellip[4] = (180 - one_ellip[4]) / 180 * pi
        ell = ellipse_pnt(one_ellip)
        p = Polygon(ell.T, color=colors[int(one_ellip[5])], label=colors[int(one_ellip[5])])
        handle[colors[int(one_ellip[5])]] = ax1.add_patch(p)

    ax1.set_xlim([200, 2305])
    ax1.set_ylim([100, 2300])
    ax1.set_aspect('equal', 'box')
    ax1.set_xticklabels([])
    ax1.set_xticks([])
    ax1.set_yticklabels([])
    ax1.set_yticks([])
    or_patch = mpatches.Patch(color='orange', label='CC')
    gr_patch = mpatches.Patch(color='green', label='MCC')
    bl_patch = mpatches.Patch(color='blue', label='SLD')
    re_patch = mpatches.Patch(color='red', label='SLP')
    ax1.legend(handles=[or_patch, gr_patch, bl_patch, re_patch], loc=3)

    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.close()