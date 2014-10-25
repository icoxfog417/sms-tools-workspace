import os
import sys
import numpy as np
from scipy.signal import get_window
import matplotlib.pyplot as plt
import math

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import stft as STFT
import utilFunctions as UF

eps = np.finfo(float).eps

"""
A4-Part-4: Computing onset detection function (Optional)

Write a function to compute a simple onset detection function (ODF) using the STFT. Compute two ODFs one 
for each of the frequency bands, low and high. The low frequency band is the set of all the frequencies 
from 0 - 3000 Hz and the high frequency band is the set of all the frequencies from 3000 - 10000 Hz. 

A brief description of the onset detection function can be found in the pdf document (A4-STFT.pdf, in 
Relevant Concepts section) in the assignment directory (A4). Start with an initial condition of 
ODF(0) = 0 in order to make the length of the ODF same as that of the energy envelope. Remember to 
apply a half wave rectification on the ODF. 

The input arguments to the function are the wav file name including the path (inputFile), window type (window),
window length (M), FFT size (N), and hop size (H). The function should return a numpy array with two columns, 
where the first column is the ODF computed on the low frequency band and the second column is the ODF computed
on the high frequency band.

Use stft.stftAnal() to obtain the STFT magnitude spectrum for all the audio frames. Then compute two 
energy values for each frequency band specified. While calculating frequency bins for each frequency band,
consider only the bins that are within the specified frequency range. For example, for the low frequency 
band consider only the bins with frequency > 0 Hz and < 3000 Hz. This way we also remove the DC offset in 
the signal in energy envelope computation.

To get a better understanding of the energy envelope and its characteristics you can plot the envelopes 
together with the spectrogram of the signal. You can use matplotlib plotting library for this purpose. 
To visualize the spectrogram of a signal, a good option is to use colormesh. You can reuse the code in
sms-tools/lectures/4-STFT/plots-code/spectrogram.py. Either overlay the envelopes on the spectrogram 
or plot them in a different subplot. Make sure you use the same range of the x-axis for both the 
spectrogram and the energy envelopes.

EXAMPLE: Running your code on piano.wav file with window = 'blackman', M = 513, N = 1024, H = 128 in 
the plots you can clearly notice that ODF have sharp peaks at the onset of the piano notes (See figure in 
the accompanying pdf). You will get exactly 6 peaks that are above 10 dB value in the ODF computed on the 
high frequency band. 
"""

def computeODF(inputFile, window, M, N, H):
    """
    Inputs:
            inputFile (string): input sound file (monophonic with sampling rate of 44100)
            window (string): analysis window type (choice of rectangular, triangular, hanning, hamming, 
                blackman, blackmanharris)
            M (integer): analysis window size (odd integer value)
            N (integer): fft size (power of two, bigger or equal than than M)
            H (integer): hop size for the STFT computation
    Output:
            The function should return a numpy array with two columns, where the first column is the ODF 
            computed on the low frequency band and the second column is the ODF computed on the high 
            frequency band.
            ODF[:,0]: ODF computed in band 0 < f < 3000 Hz 
            ODF[:,1]: ODF computed in band 3000 < f < 10000 Hz
    """
    
    ### your code here
    def energy(mag):
        e = 10 * np.log10(np.sum((10 ** (mag / 20)) ** 2, axis=1))
        return e

    def odf(eg):
        o = eg - np.roll(eg, 1)
        o[0] = 0
        o[o <= 0] = 0
        return o

    (fs, x) = UF.wavread(inputFile)
    border_bin = int(np.ceil(float(3000) * N / fs))
    max_bin = int(np.ceil(float(10000) * N / fs))
    w = get_window(window, M)
    
    mX, pX = STFT.stftAnal(x, fs, w, N, H)
    low = np.transpose(np.transpose(mX)[1:border_bin])
    high = np.transpose(np.transpose(mX)[border_bin:max_bin])
    
    odf_low = odf(energy(low))
    odf_high = odf(energy(high))    
    
    odfs = np.append([odf_low], [odf_high], axis=0)
    odfs = np.transpose(odfs)
    
    # draw graph
    plt.figure(1, figsize=(9.5, 6))

    plt.subplot(211)
    numFrames = mX.shape[0]
    frmTime = H*np.arange(numFrames)/float(fs)
    binFreq = np.arange(mX.shape[1])*float(fs)/N
    plt.pcolormesh(frmTime, binFreq, np.transpose(mX))
    plt.title('mX ({0}), M={1}, N={2}, H={3}'.format(inputFile, M, N, H))
    plt.autoscale(tight=True)
    
    plt.subplot(212)
    plt.plot(frmTime, odf_low, color="blue", label="row")
    plt.plot(frmTime, odf_high, color="red", label="high")
    plt.title('Onset Detection function')
    plt.autoscale(tight=True)

    plt.tight_layout()
    plt.show()

    return odfs
