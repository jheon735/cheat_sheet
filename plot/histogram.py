import numpy as np
import matplotlib.pyplot as plt

bins = np.linspace(min(data), max(data), 20)
hist, bins = np.histogram(data, bins)
x = (bins+(bins[1] - bins[2])/2)[:-1]
plt.plot(x, hist/hist.sum(), label = 'label name', linestyle='--')  #선 히스토그램
plt.hist(data, bins=30, alpha=0.3, label='total', density=True)     #막대 히스토그램

plt.legend()
plt.title(f'title')
plt.tight_layout()
plt.savefig(f'directory')
plt.close()
