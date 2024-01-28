import datetime
import numpy as np

def id_gen():
    """
    고유 ID를 만들어주는 함수
    :return:
    """
    count = 0
    while True:
        count +=1
        yield count

gen = id_gen()
for i, fname in enumerate(flist):
    strtime = fname.split('\\')[-1].split('.')[0][-12:]
    dtime = datetime.datetime.strptime(strtime, "%Y%m%d%H%M")
    data = np.genfromtxt(fname, skip_header=5, skip_footer=1)
    len_data = len(data)
    pid = data[:, 0]
    # 이전 파일의 id를 비교하며 고유 ID 생성
    if i == 0:
        fid = np.array([next(gen) for i in range(len_data)])
        data = np.hstack((fid.reshape(len_data, 1), data))
        ndata = np.pad(data, ([0, 0], [1, 0]), 'constant', constant_values=(int(strtime)))
    else:
        if dtime - datetime.datetime.strptime(flist[i-1].split('\\')[-1].split('.')[0][-12:],  "%Y%m%d%H%M") == datetime.timedelta(minutes=10):
            nnid = np.zeros(len_data)
            nnid[pid ==-999] = [next(gen) for i in range((pid==-999).sum())]
            nnid[pid != -999] = [fid[int(j)] for j in pid if j != -999]
            fid = nnid
            data = np.hstack((fid.reshape(len_data, 1), data))
        else:
            fid = np.array([next(gen) for i in range(len_data)])
            data = np.hstack((fid.reshape(len_data, 1), data))
        # 고유 ID와 시간을 추가하여 새로운 데이터 어레이 생성
        data = np.pad(data, ([0, 0], [1, 0]), 'constant', constant_values=(int(strtime)))
        ndata = np.vstack((ndata, data))
