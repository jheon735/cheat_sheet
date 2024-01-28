import numpy as np

A=np.arange(10)
fft = np.fft.fftshift(np.fft.fft(A)) #shift를 해야 frequency 0이 중앙에 위치

A=np.ones([10,10])
fft = np.fft.fftshift(np.fft.fft2(A)) #2차원 FFT

print(fft)