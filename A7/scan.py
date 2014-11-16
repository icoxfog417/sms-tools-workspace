import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import sineModel as SM
import harmonicModel as HM
import stft

eps = np.finfo(float).eps

def estimate(inputFile = 'a7q2-harmonic.wav', window='blackman', M=2101, N=4096, t=-90, 
    minSineDur=0.1, nH=50, minf0=100, maxf0=200, f0et=5, harmDevSlope=0.01):
    
    Ns = 512
    H = 128
    
    fs, x = UF.wavread(inputFile)
    w  = get_window(window, M)
    hfreq, hmag, hphase = HM.harmonicModelAnal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur)
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)
    y = SM.sineModelSynth(hfreq, hmag, hphase, Ns, H, fs)
    
    # plt.plot(x)
    # plt.plot(y)
    # plt.show()
    
    size = min([x.size, y.size])
    diff = np.sum(np.abs(x[:size] - y[:size]))
    std = np.std(f0)
    
    print "diff:{0} & std:{1}, M={2} N={3} t={4} minSineDur={5} nH={6} min/max={7}/{8} f0et={9} harmDevSlope={10}" \
    .format(diff, std, M, N, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)
    
    return diff, std
    
if __name__ == "__main__":
    parameters = []
    diffs = []
    stds = []
    
    # Part1
    # parameters.append({"inputFile":"speech-female.wav","M":2001, "N":4096,"t":-80, "minSineDur":0.1, "nH":33, "minf0":146, "maxf0":222, "harmDevSlope":0.01})

    # Part2
    # parameters.append({"M":2101, "N":4096,"t":-72, "minSineDur":0.01, "nH":46, "minf0":103, "maxf0":212, "harmDevSlope":0.014})
  
    for p in parameters:
        diff, std = estimate(**p)
        diffs.append(diff)
    
    plt.plot(diffs)
    plt.show()
