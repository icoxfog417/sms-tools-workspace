7A Peer-Assessment: Sinusoidal plus residual
========= 

## Brief description of the analysis parameters

* Window type (window) and Window size (M): The choice of window size and window type has a time-frequency trade-off. Choosing a longer window helps resolve sinusoidal components that are close in frequency, but gives a poorer temporal resolution. Shorter windows track transients better, giving us sharp onsets, but may not resolve frequency components so well. For monophonic harmonic sounds, the window size is best chosen based on the lowest value of f0 and the fastest change in pitch. 
* FFT size (N): The FFT size is typically chosen as a power of 2 larger than the window size M. A large FFT size interpolates the DFT spectrum and hence leads to better estimation of spectral peak values. However, given that the software also uses parabolic interpolation we can achieve good peak estimates with smaller FFT sizes. 
* Threshold in negative dB (t): The peak picking threshold is the lowest amplitude peak that will be identified. Setting a very low threshold (<-120dB) will take most peaks, but the threshold should be set as high as possible to minimize the presence of peaks that do not correspond to sinusoidal peaks (the window main-lobe). 
* Maximum number of harmonics (nH): The maximum number of harmonics that can be detected in a harmonic sound is influenced by the brightness of the sound, but also to the sampling rate and by how low is the f0.  The recording quality can also have an impact. For a compact representation, we should only capture the relevant harmonics, thus only the ones that affect the perceptual quality of the reconstruction. 
* Minimum f0 frequency in Hz (minf0) and Maximum f0 frequency in Hz (maxf0): The minf0 and maxf0 are the parameters used by the fundamental frequency detection algorithm to obtain possible f0 candidates to be passed to the TWM algorithm. Choosing a correct range of f0 greatly improves the f0 estimation by TWM algorithm, specially minimizing octave errors, which are very common in f0 detection algorithms. You should use the smallest range possible by first looking at the spectrogram of the sound and identifying the lowest and highest fundamental frequencies present.
* Error threshold in the f0 detection (f0et): Error threshold in the f0 detection. This is the maximum error allowed in the TWM algorithm. If the TWM mismatch error is larger than f0et, no f0 is detected and the TWM algorithm returns f0 = 0 for the frame.  The smaller this value the more restrictive the algorithm will behave. A normal strategy is to start with a big value (> 10) and then making it smaller until we only keep the relevant f0 components and discard the f0 values in the parts of the sound that do not have a clear harmonic structure.
* Slope of harmonic deviation (harmDevSlope): Slope of harmonic deviation allowed in the estimated harmonic frequency, compared to a perfect harmonic frequency. If the value is 0 it means that we allow the same deviation for all harmonics, which is hard coded to f0/3. A value bigger than 0 means that higher harmonics will be allowed to deviate more than the lower harmonics. It normally works better to have a value slightly bigger than 0, for example around 0.01.
* Minimum length of harmonics (minSineDur): Any harmonic track shorter, in seconds, than minSineDur will be removed. This is a good parameter to discard harmonic tracks that are too short and thus do not correspond to a stable harmonic of the sound. Typically we would put a value bigger that 0.02 seconds.
* Decimation factor of magnitude spectrum for stochastic analysis (stocf): The stochastic approximation of the residual uses a decimated version of the magnitude spectrum of the residual. This leads to a compact and smooth function that approximates the magnitude spectrum of the residual at each frame. The smaller the stocf, higher the decimation will be and thus will result in a more compact representation.  A value of 1 means no decimation, leaving the residual magnitude spectrum as it is. A value of 0.2 (a good starting value) will decimate the original residual magnitude spectrum by a factor of 1/5. 

## Question 1. Obtain a good harmonic+stochastic analysis of a speech sound

### Part 1.1
(max magnitude(dB), pitch range that seems to be f0, assumption of harmonics count)

### Part 1.2
* window type:
* window size:
* FFT size:
* minimum f0:
* maximum f0:
* error threshold in f0 detection:
* number of harmonics:
* stochastic decimation factor:

speech-harmonic: [speech-harmonic.wav]()  
speech-stochastic: [speech-stochastic.wav]()  
speech-reconstructed: [speech-reconstructed.wav]()

## Question 2. Obtain a good harmonic+stochastic analysis of a monophonic musical phrase 

### Part 2.1
[selected sound from free sound:]()
(describe why you choosed it.)

### Part 2.2
(max magnitude(dB), pitch range that seems to be f0, assumption of harmonics count)

### Part 2.3
* window type:
* window size:
* FFT size:
* minimum f0:
* maximum f0:
* error threshold in f0 detection:
* number of harmonics:
* stochastic decimation factor:

a7q2-harmonic: [a7q2-harmonic.wav]()  
a7q2-stochastic: [a7q2-stochastic.wav]()  
a7q2-reconstructed: [a7q2-reconstructed.wav]()
