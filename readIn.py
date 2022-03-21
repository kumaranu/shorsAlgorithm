import numpy as np
from glob import glob

def readIn(referenceDir):
    dirList = glob(referenceDir + '/0.*')
    svrList = np.asarray(sorted([np.float(directory.split('/')[-1]) for directory in dirList]))
    svrListStr = [directory.split('/')[-1] for directory in dirList]
    
    sortedStrSvr = []
    for i in svrList:
        for j in svrListStr:
            if str(i) == j:
                sortedStrSvr.append(j)
    return sortedStrSvr

def readIn1(referenceDir, svr):
    leftVectorsFile = referenceDir + '/' + svr + '/fort.101'
    leftVectors = np.loadtxt(leftVectorsFile)
    singularValuesFile = referenceDir + '/' + svr + '/fort.201'
    singularValues = np.loadtxt(singularValuesFile)
    rightVectorsFile = referenceDir + '/' + svr + '/fort.301'
    rightVectors = np.loadtxt(rightVectorsFile)
    return [leftVectors, singularValues, rightVectors]


