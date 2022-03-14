import random
import numpy as np

#initialization
nSteps, nTerms = 5, 3
v = np.asarray([0.4, 0.1, 0.01])

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

