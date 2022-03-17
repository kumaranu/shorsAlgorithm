import random, matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, ifft
from glob import glob
import sys
from pathlib import Path

np.set_printoptions(suppress=True)
#initialization
referenceDir = '/N/project/ctm/From-Nicole/2D'
dirList = glob(referenceDir + '/0.*')
svrList = np.asarray(sorted([np.float(directory.split('/')[-1]) for directory in dirList]))
svrListStr = [directory.split('/')[-1] for directory in dirList]

sortedStrSvr = []
for i in svrList:
    for j in svrListStr:
        if str(i) == j:
            sortedStrSvr.append(j)

for svr in sortedStrSvr:
    try:
        print('Entering the SVR =', svr, 'case.')
        leftVectorsFile = referenceDir + '/' + svr + '/fort.101'
        leftVectors = np.loadtxt(leftVectorsFile)
        for i in range(np.shape(leftVectors)[1]):
            fft_leftVector = fft(leftVectors[:, i])
        print('Done with the SVR =', svr, 'case.\n')
    except:
        print('Some problem in SVR = ', svr, 'case.')

sys.exit()

#Calculating fourier transform
fft_leftVectors0 = fft(leftVectors[:, 0])
fft_leftVectors1 = fft(leftVectors[:, 1])
fft_leftVectors2 = fft(leftVectors[:, 2])
fft_leftVectors3 = fft(leftVectors[:, 3])
fft_leftVectors4 = fft(leftVectors[:, 4])
fft_leftVectors5 = fft(leftVectors[:, 5])

# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
ax.plot(leftVectors[:, 0]*627.503, label='1st singular vector')
ax.plot(leftVectors[:, 1]*627.503, label='2nd singular vector')
ax.plot(leftVectors[:, 2]*627.503, label='3rd singular vector')
ax.plot(leftVectors[:, 3]*627.503, label='4th singular vector')
ax.plot(leftVectors[:, 4]*627.503, label='5th singular vector')
ax.plot(leftVectors[:, 5]*627.503, label='6th singular vector')
#ax.plot(leftVectors[:, 5]*627.503, label='6th singular vector', color="red", marker="o", markersize=1)
# set x-axis label
ax.set_xlabel("R",fontsize=14)
# set y-axis label
ax.set_ylabel("singular vectors",color="red",fontsize=14)
ax.legend()
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(fft_leftVectors0)
ax2.plot(fft_leftVectors1)
ax2.plot(fft_leftVectors2)
ax2.plot(fft_leftVectors3)
ax2.plot(fft_leftVectors4)
ax2.plot(fft_leftVectors5)
ax2.set_ylabel("fft", color="blue", fontsize=14)
#plt.show()
# save the plot as a file
fig.savefig('funtionFft.png', format='png', dpi=100, bbox_inches='tight')

#plt.plot(leftVectors[:, 0], label='first singular vector')
#plt.plot(fft_leftVectors, label='fft')
#plt.xlabel('x')
#plt.ylabel('')
#plt.legend()
#plt.draw()
#plt.show()

#nSteps, nTerms = 5, 3
#v = np.asarray([0.4, 0.1, 0.01])
#x = np.arange(99)
#f1 = np.exp(-(x-1)**2) + np.exp(-x**2)
#
##normalization and binning
#normalized_v = v / np.sqrt(np.sum(v**2))
#tempSum, binList = 0.0, []
#for i in normalized_v**2:
#    tempSum += i
#    binList.append(tempSum)
#binList = np.asarray(binList)
#
#for i in range(nSteps):
#    random.seed(i)
#    n = random.random()
#    for j in range(nTerms):
#        if n < binList[j]:
#            print(n, i, j)
#
#fft_x = fft(f1)
#plt.plot(x, f1, label='linear')
#plt.plot(x, fft_x.real, label='fft_real')
#plt.plot(x, fft_x.imag, label='fft_imag')
#plt.xlabel('x')
#plt.ylabel('')
#plt.legend()
#plt.show(block='False')
#
#plt.show()


