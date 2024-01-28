import numpy as np

data = np.zeros(100)
even = np.array(data[::2])
odd = np.array(data[1::2])
even = np.reshape(even, (5, 1, 2, 5))
even = np.moveaxis(even, -1, 0)  #축 전환
even = np.mean(even, axis=3)  #3번째 축으로 평균

A = np.ones([10, 10])
B = np.ones([10, 10])
C = np.multiply(A, B) #행렬곱

D = np.delete(A, [0, 3, 5], axis = 0)  #행렬에서 특정 열 혹은 행 제거
