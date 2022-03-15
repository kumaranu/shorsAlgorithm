import random
import numpy as np
from scipy.fft import fft, ifft

#initialization
nSteps, nTerms = 5, 3
v = np.asarray([0.4, 0.1, 0.01])
x = np.arange(99)
f1 = np.exp(-(x-1)**2) + np.exp(-x**2)
f2 = np.exp(-(x-2)**2) + np.exp(-x**2)

#normalization and binning
normalized_v = v / np.sqrt(np.sum(v**2))
tempSum, binList = 0.0, []
for i in normalized_v**2:
    tempSum += i
    binList.append(tempSum)
binList = np.asarray(binList)

for i in range(nSteps):
    random.seed(i)
    n = random.random()
    for j in range(nTerms):
        if n < binList[j]:
            print(n, i, j)

fft_x = fft(f1)
print(fft_x)
