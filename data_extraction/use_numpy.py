import numpy as np

A = np.ones([10, 10])
B = np.ones([10, 10])

C = np.hstack((A, B)) #세로로 쌓기
D = np.vstack((A, B)) #가로로 쌓기

data = np.pad(A, ([0, 1], [1, 0]), 'constant', constant_values=0)   #[위, 아래], [왼쪽, 위] 특정 상수 값으로 추가
