import random, matplotlib.pyplot as plt
import numpy as np

def figurePlottingFn(fnVector,fft_Vector, index1, index2):
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots()
    ax.plot(fnVector*627.503, label='singular vector-'+str(index2), color='red')
    ax.set_xlabel("R", fontsize=14)
    ax.set_ylabel("singular vector", color="red", fontsize=14)
    ax.legend()
    ax2=ax.twinx()
    ax2.plot(fft_Vector.real, label='fft-' + str(index2), color='blue')
    ax2.set_ylabel("fft", color="blue", fontsize=14)
    ax2.legend()
    #plt.show()
    fig.savefig('fft-' + str(index1) + '-' + str(index2) + '.png', format='png', dpi=100, bbox_inches='tight')


