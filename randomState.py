import random, matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, ifft
from glob import glob
import sys
from pathlib import Path
from readIn import readIn, readIn1
from figurePlottingFn import figurePlottingFn

def genBinList(singularValues, nSteps, svr):
    print("a1")
    #normalization and binning
    normalized_sv = singularValues / np.sqrt(np.sum(singularValues ** 2))
    print("a2")
    tempSum, binList = 0.0, []
    for i in normalized_sv**2:
        tempSum += i
        binList.append(tempSum)
    print("a3")
    binList = np.asarray(binList)

    for i in range(nSteps):
        random.seed(svr * i)
        n = random.random()
        print("a4")
        for j in range(len(singularValues)):
            print("binList[j:(j+1)]:", binList[j:(j+1)])
            if n < binList[j:(j+1)]:
                print("Step #, bin #, random #:", i, j, n)


