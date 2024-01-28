import numpy as np

a = np.array([1+3j, 1-3j])
a = np.conjugate(a) #conjugate, array, list, 단일 모두 가능
real, imag = a.real, a.imag

