import random, matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, ifft
from glob import glob
import sys
from pathlib import Path
from readIn import readIn, readIn1
from figurePlottingFn import figurePlottingFn
from randomState import genBinList

#initialization
referenceDir = '/N/project/ctm/From-Nicole/2D'
nSteps = 2

def main():
    sortedStrSvr = readIn(referenceDir)
    for svr in sortedStrSvr[1:2]:
        try:
            print('\nEntering the SVR =', svr, 'case.')
            leftVectors, singularValues, rightVectors = readIn1(referenceDir, svr)
            binList = genBinList(singularValues, nSteps, svr)

            ##for i in range(np.shape(leftVectors)[1]):
            ##    fft_leftVector = fft(leftVectors[:, i])
            ##    figurePlottingFn(leftVectors[:, i], fft_leftVector, svr, i)
            print('Done with the SVR =', svr, 'case.')
        except:
            print('Some problem in SVR = ', svr, 'case.')
    #sys.exit()

if __name__ == "__main__":
    main()


