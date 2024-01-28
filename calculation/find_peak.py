import numpy as np

def peakRange(data_spc, noise_level, select_index=None):
    if select_index is not None:
        maxind = select_index
    else:
        maxind = np.argmax(data_spc)
    loval = data_spc[maxind]
    loind = maxind
    hival = data_spc[maxind]
    hiind = maxind

    try:
        while loval > noise_level and loind >= 0:
            loind -= 1
            loval = data_spc[loind]

        loind -= 1
    except:
        loind = 0

    try:
        while hival > noise_level:
            hiind += 1
            hival = data_spc[hiind]

        hiind += 1
    except:
        hiind = len(data_spc) - 1

    testResult = data_spc[loind + 1:hiind] - noise_level
    testnum = hiind - loind - 1
    return testResult, testnum, loind, hiind