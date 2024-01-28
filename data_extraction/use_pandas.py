import numpy as np
import pandas as pd

data_pd = pd.DataFrame(data, columns=["col1", "col2", "col3"])

# 고유ID로 학습자료, 검증자료 구분
new_data_pd = data_pd[data_pd.Type == 0].drop_duplicates(subset=['ID'])  #전체 자료에서 원하는 타입 가져온 후 중복 제거
A = new_data_pd["A"].values     #특정 컬럼 값 가져오기
test_pid = np.append(cc_pid, np.append(mcc_pid, np.append(sld_pid, np.append(slp_pid, na_pid))))

part_pd = data_pd["col1", "col2"]       #일부 컬럼만 가져오기
part_pd = part_pd.dropna()  #nan값 제거
part_pd = part_pd[part_pd.Type != 3]    #특정 컬럼의 특정 값 아닌 부분만
