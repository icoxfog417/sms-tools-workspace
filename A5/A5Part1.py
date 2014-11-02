import numpy as np
from scipy.signal import get_window
import math
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import dftModel as DFT
import utilFunctions as UF
import matplotlib.pyplot as plt

""" 
A5-Part-1: Minimizing the frequency estimation error of a sinusoid

Write a function that estimates the frequency of a sinusoidal signal at a given time instant. The 
function should return the estimated frequency in Hz, together with the window size and the FFT 
size used in the analysis.  

The input arguments to the function are the wav file name including the path (inputFile) containing 
the sinusoidal signal, and the frequency of the sinusoid in Hz (f). The frequency of the input sinusoid  
can range between 100Hz and 2000Hz. The function should return a three element tuple of the estimated 
frequency of the sinusoid (fEst), the window size (M) and the FFT size (N) used.

The input wav file is a stationary audio signal consisting of a single sinusoid of length 1 second. 
Since the signal is stationary you can just perform the analysis in a single frame, for example in 
the middle of the sound file (time equal to .5 seconds). The analysis process would be to first select 
a fragment of the signal equal to the window size, M, centered at .5 seconds, then compute the DFT 
using the dftAnal function, and finally use the peakDetection and peakInterp functions to obtain the 
frequency value of the sinusoid.

Use a Blackman window for analysis and a magnitude threshold t = -40 dB for peak picking. The window
size and FFT size should be chosen such that the difference between the true frequency (f) and the 
estimated frequency (fEst) is less than 0.05 Hz for the entire allowed frequency range of the input 
sinusoid. The window size should be the minimum positive integer of the form 100*k + 1 (where k is a 
positive integer) for which the frequency estimation error is < 0.05 Hz. For a window size M, take the
FFT size (N) to be the smallest power of 2 larger than M. 

HINT: If the specified frequency range would have been 440-8000 Hz, the parameter values that satisfy 
the required conditions would be M = 1101, N = 2048. Note that for a different frequency range, like 
the one specified in the question, this value of M and N might not work. 

"""
def minFreqEstErr(inputFile, f):
    """
    Inputs:
            inputFile (string) = wav file including the path
            f (float) = frequency of the sinusoid present in the input audio signal (Hz)
    Output:
            fEst (float) = Estimated frequency of the sinusoid (Hz)
            M (int) = Window size
            N (int) = FFT size
    """
    # analysis parameters:
    window = 'blackman'
    t = -40
    
    ### Your code here
    (fs, x) = UF.wavread(inputFile)
    
    ## search best window size between 100 - 2000Hz
    fEst = 0.0
    M = 0
    N = 0
    
    def peak(m, n):
        hfs = fs * 0.5
        x1 = x[hfs-m/2:hfs+(m+1)/2]
        w = get_window(window, m)
        mX, pX = DFT.dftAnal(x1, w, n)
        
        ploc = UF.peakDetection(mX, t)
        iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)
        fest = fs * iploc[0] / n
        return fest, ploc, mX, pX
    
    # search best window size for 100 - 2000Hz
    # (to analyze 2000Hz, max window size is twice)
    baseM = 6.0 * fs / f # blackman window's bin is 6.
    k = int(baseM // 100)
    min_diff = 1
    for k in range(k, 41):
        localM = k * 100 + 1 # M is 100 * k + 1 value ordinary.
        localN = int(2 ** (np.ceil(np.log2(localM))))
        
        # apply local M and N to every frequency and calculate difference between real freq.
        fEst, lploc, lmx, lpx = peak(localM, localN)
        diff = np.abs(fEst - f)
        
        if diff < 0.05:
            print("M&N pair below 0.05 = {0}&{1} (diff={2})".format(localM, localN, diff))
            if diff < min_diff:
                M = localM
                N = localN
                min_diff = diff
            
    print("best value in freq {0} is M={1}, N={2} (diff={3})".format(f, M, N,min_diff))

    #calculate by best M & N (every calculation is done in above, set fix value in below)
    M = 2101
    N = 4096
    fEst, gploc, gmX, gpX = peak(M, N)

    hN = N/2
    p, pmg, ph = UF.peakInterp(gmX, gpX, gploc)
    freqaxis = fs*np.arange(hN+1)/float(N)
    plt.plot(freqaxis,gmX,'r', lw=1.5)
    plt.axis([100,2000,-70,max(gmX)])
    plt.plot(fs * p / N, pmg, marker='x', color='b', linestyle='', markeredgewidth=5)
    plt.title('mX + spectral peaks ({0})'.format(inputFile))
    plt.show()

    return fEst, M, N
