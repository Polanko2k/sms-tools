import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from scipy.fftpack import fft, ifft

a = 0.5
b = 1.0
k1 = 20
k2 = 25
N = 128
x1 = a*np.exp(1j*2*np.pi*k1/N*np.arange(N))
x2 = b*np.exp(1j*2*np.pi*k2/N*np.arange(N))
plt.figure(1)
plt.subplot(321)
plt.title('x1 (amp=.5, freq=20)')
plt.plot(np.arange(0, N, 1.0), np.real(x1))
plt.axis([0, N, -1, 1])

plt.subplot(322)
plt.title('x2 (amp=1, freq=25)')
plt.plot(np.arange(0, N, 1.0), np.real(x2))
plt.axis([0, N, -1, 1])
X1 = fft(x1)
mX1 = abs(X1)/N        

plt.subplot(323)
plt.title('X1 (amp=.5, freq=20)')
plt.plot(np.arange(0, N, 1.0), mX1)
plt.axis([0,N,0,1])
X2 = fft(x2)
mX2 = abs(X2)/N        

plt.subplot(324)
plt.title('X2 (amp=1, freq=25)')
plt.plot(np.arange(0, N, 1.0), mX2)
plt.axis([0,N,0,1])
x = x1 + x2

plt.subplot(325)
plt.title('X1+X2')
plt.plot(np.arange(0, N, 1.0), mX1+mX2)
plt.axis([0, N, 0, 1])
X = fft(x)
mX= abs(X)/N        

plt.subplot(326)
plt.title('DFT(x1+x2)')
plt.plot(np.arange(0, N, 1.0), mX)
plt.axis([0,N,0,1])

plt.show()