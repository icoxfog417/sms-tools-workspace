9A Peer-Assessment: Sound and music description
========= 
## About sound description

### Energy, RMS, Loudness

* RMS is Root mean square
* Loudness is calculated by Steven's power law

These features represent the loudness (like stroke of note and so on).  

### Spectral centroid
It related with the impression of brightness of sound.  

### Dissonance
The auditory experience of sound that lacks musical quality.  
Like white noise?

### HFC
HFC is High Frequency Content. As its name, it is used to characterize the amount of high-frequency content in the signal.  
It doesn't so relate to human hearing, but useful to detect the onset.   

### Logattacktime
The log (base 10) of the attack time of a signal envelope.  
The attack time is defined as the time duration from when the sound becomes perceptually audible to when it reaches its maximum intensity.

### Inharmonicity
Degree of the separation from the harmony.
The inharmonicity value is computed as an energy weighted divergence of the spectral components from their closest multiple of the fundamental frequency. 

### Spectral contrast
The strength of spectral peaks and spectral valleys in each frame.  
So that it could represent the relative spectral characteristics, and then roughly reflect the distribution of harmonic and non-harmonic components.  

[MUSIC TYPE CLASSIFICATION BY SPECTRAL CONTRAST FEATURE](http://hcsi.cs.tsinghua.edu.cn/Paper/Paper02/200218.pdf)

### MFCC
MFCC is Mel frequency cepstral coefficients.  
It is the kind of cepstrum analysis that FFT the FFT result to separate the sound source and vocal cord.  
Thus, this feature is used to analyze the voice.  
Usually, mfcc has 12 coefficients.  
The first one describes the bigger picture of spectrum, and as we go higher up, it describes more detail, small changes in the spectrum. 

Mel scale is the scale for human. Human can hear lower frequency than higher.  
So frequency becomes higher , the rate of increase in mel scale becomes lower.  

### pitch salience
The pitch of sound. It is useful to characterize quite a number of sound.

### Chroma(Harmonic Pitch Class Profile)
It represents inherent circularity of pitch of organization.  
The same pitch notes in different octaves have the same chroma.  
It is useful to separate the many instruments in the sound.  

## Task 1: Download sounds and descriptors from Freesound
To access api, you have to create key from [here](http://www.freesound.org/apiv2/apply/).

### Get sounds
SD.downloadSoundsFreesound(queryText='violin',API_Key='-', outputDir='freesound', topNResults=20,duration=(0,5), tag=['spiccato','pizzicato'])
SD.downloadSoundsFreesound(queryText='bassoon',API_Key='-', outputDir='freesound', topNResults=20,duration=(0,5), tag=['staccato'])
SD.downloadSoundsFreesound(queryText='clarinet',API_Key='-', outputDir='freesound', topNResults=20,duration=(0,5), tag=['single-note'])

### Description
I choose the instruments that have many single-note examples.  
And there are some technique to play one and short sound (like spiccato).

1. violin
 * query text: violin
 * tag: pizzicato
 * duration: (0,5)

2. bassoon
 * query text: bassoon
 * tag: staccato
 * duration: (0,5)

3. clarinet
 * query text: clarinet_pablo_proj
 * tag: single-note
 * duration: (0,5)
The sounds of clarinet_pablo_proj was very good.
 
## Task 2: Select two descriptors for a good clustering of sounds in 2D
### Descriptor pairts.

* 9 -- lowlevel.spectral_contrast.mean.4
* 14 -- lowlevel.mfcc.mean.3 

and 

* 5 -- lowlevel.spectral_contrast.mean.0
* 14 -- lowlevel.mfcc.mean.3

It is the problem of detecting the feature of instruments.  
So I used the descriptors that can represent the characteristics of the timbre(especially harmony). It likes the spectral_contrast, mfcc.  
Oppositely, I removed the descriptors that are influenced by playing (like logattacktime).  
And these instruments has good harmony, so I didn't use the descriptors relate to inharmony(dissonance, inharmonicity).  

## Task 3: Cluster sounds of different instruments using kmeans in n-dimensions
### Descriptors
* 10 -- lowlevel.spectral_contrast.mean.5
* 13 -- lowlevel.mfcc.mean.2
* 14 -- lowlevel.mfcc.mean.3

SA.clusterSounds("freesound", nCluster=3, descInput=[10,13,14])

### Accuracy
100%

### Opinion
The sound of the bassoon and clarinet is very similar, especially in low frequency.  
And to separate these, MFCC parameter was very effective.  
MFCC is commonly used in speech recognition. It means that MFCC is very effective to classify the harmonic sound.
Bassoon and clarinet have harmonic sound also, so MFCC may works well.  

I also tried the below (but it didn't worked well as above).
* Task2 parameter(9,14): 95%. It couldn't separate the basson and clarinet at low frequency.
* Task2 parameter(5,14): 91.67%(3 cluster), 98.33(4 cluster). lowlevel.spectral_contrast.mean.0 separates the clarinet into two group. so 4 cluster works very well.
* use spectral_centroid: around 90%

## Task 4: Classify a sound by using descriptors and a nearest neighbor classifier
### Download test sound
* SD.downloadSoundsFreesound(queryText='cello',API_Key='-', outputDir='knn', topNResults=5,duration=(0,3), tag='pizzicato')
* SD.downloadSoundsFreesound(queryText='guitar',API_Key='-', outputDir='knn', topNResults=5,duration=(0,3), tag='acoustic')
* SD.downloadSoundsFreesound(queryText='slothrop',API_Key='-', outputDir='knn', topNResults=5,duration=(0,3), tag='trumpet')
* SD.downloadSoundsFreesound(queryText='naobo',API_Key='-', outputDir='knn', topNResults=5,duration=(0,3))
* SD.downloadSoundsFreesound(queryText='bassoon',API_Key='-', outputDir='knn', topNResults=5,duration=(0,3), tag='multiphonic')

### Parameters
* descriptors:10,13,14
* K:3

Above parameters are most accurate in Task3.

### Classification
1. cello sound:https://www.freesound.org/people/Corsica_S/sounds/42256/  
=> belongs to 'violin'
2. guitar https://www.freesound.org/people/hubertmichel/sounds/40472/  
=> belongs to 'violin'
3. trumpet: https://www.freesound.org/people/slothrop/sounds/48223/  
=> belongs to 'clarinet'
4. naobo: https://www.freesound.org/people/ajaysm/sounds/222275/  
=> belongs to 'clarinet'
5. basson https://www.freesound.org/people/tewell/sounds/90023/  
=> belongs to 'basson'

cello and guitar is similar to violin (stringed instrument), so classification is well.  
trumpet and naobo is not so similar to clarinet (especially naobo), but in 3 instruments, clarinet may be closest.
I used basson sound that different enough from the existing sounds, but it can classify it.
