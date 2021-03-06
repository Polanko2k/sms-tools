import numpy as np
import time, os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../../code/basicFunctions/'))

import smsWavplayer as wp
import smsPeakProcessing as PP
from scipy import signal
import matplotlib.pyplot as plt
import math
from numpy.fft import fft

def sineModelPlot(x, fs, w, N, H, t, minFreq, maxFreq):
    ''' Analysis/synthesis of a sound using the short-time fourier transform
    x: input array sound, w: analysis window, N: FFT size, H: hop size
    YSpec: The STFT of x (Only the half spectrum is stored)'''
   
    hN = N/2                                                # size of positive spectrum
    hM1 = int(math.floor((w.size+1)/2))                     # Ceil of half analysis window size
    hM2 = int(math.floor(w.size/2))                         # Floor of half analysis window size
    pin = hM1                                               # initialize sound pointer in middle of analysis window       
    pend = x.size-max(hM1,H)                                # last sample to start a frame
    fftbuffer = np.zeros(N)                                 # initialize buffer for FFT
    yw = np.zeros(w.size)                                   # initialize output sound frame
    y = np.zeros(x.size)                                    # initialize output array
    w = w / sum(w)                                          # normalize analysis window
    numFrames = int(math.floor(pend/float(H)))
    frmNum = 0
    frmTime = []
    firstBin = N*minFreq/float(fs)
    lastBin = N*maxFreq/float(fs)
    binFreq = np.arange(firstBin,lastBin)*float(fs)/N       # The bin frequencies
    
    while pin<pend:                                         # while sound pointer is smaller than last sample    
        frmTime.append(pin/float(fs))         
        xw = x[pin-hM1:pin+hM2]*w                             # window the input sound
        fftbuffer = np.zeros(N)                               # clean fft buffer
        fftbuffer[:hM1] = xw[hM2:]                            # zero-phase window in fftbuffer
        fftbuffer[N-hM2:] = xw[:hM2]        
        X = fft(fftbuffer)                                    # compute FFT
        mX = 20 * np.log10( abs(X[:hN]) )                     # magnitude spectrum of positive frequencies in dB     
        pX = np.unwrap(np.angle(X[:hN]))                      # unwrapped phase spectrum of positive frequencies
        ploc = PP.peakDetection(mX, hN, t)                    # detect locations of peaks
        pmag = mX[ploc]                                       # get the magnitude of the peaks
        iploc, ipmag, ipphase = PP.peakInterp(mX, pX, ploc)   # refine peak values by interpolation
        if frmNum == 0:                                       # Accumulate and store STFT
            YSpec = np.transpose(np.array([mX[firstBin:lastBin]]))
            ind1 = np.where(iploc>=firstBin)[0]
            ind2 = np.where(iploc<lastBin)[0]
            ind = list((set(ind1.tolist())&set(ind2.tolist())))
            final_peaks = iploc[ind]
            parray = np.zeros([final_peaks.size,2])
            parray[:,0]=pin/float(fs)
            parray[:,1]=final_peaks*float(fs)/N
            specPeaks = parray
        else:
            YSpec = np.hstack((YSpec,np.transpose(np.array([mX[firstBin:lastBin]]))))
            ind1 = np.where(iploc>=firstBin)[0]
            ind2 = np.where(iploc<lastBin)[0]
            ind = list((set(ind1.tolist())&set(ind2.tolist())))
            final_peaks = iploc[ind]
            parray = np.zeros([final_peaks.size,2])
            parray[:,0]=pin/float(fs)
            parray[:,1]=final_peaks*float(fs)/N
            specPeaks = np.append(specPeaks, parray,axis=0)
        pin += H
        frmNum += 1
    frmTime = np.array(frmTime)                               # The time at the centre of the frames
    plt.hold(True)
    plt.pcolormesh(frmTime,binFreq,YSpec)

    plt.scatter(specPeaks[:,0]+(0.5*H/float(fs)), specPeaks[:,1], s=10, marker='x')
    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.autoscale(tight=True)
    plt.show()
    return YSpec

# example call of sineModelPlot function
if __name__ == '__main__':
    (fs, x) = wp.wavread('../../../../sounds/sax-phrase-short.wav')
    w = np.hamming(501)
    N = 2048
    H = 500
    t = -70
    minFreq = 0
    maxFreq = fs/15.0
    YSpec = sineModelPlot(x[:40000],fs,w,N,H,t,minFreq,maxFreq)
   
