import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftshift

plt.figure(1)
M = 64
N = 64
x1 = np.hanning(M)
x2 = np.cos(2*np.pi*2/M*np.arange(M))
y1 = x1*x2
mY1 = 20 * np.log10(np.abs(fftshift(fft(y1, N))))

plt.subplot(3,2,1)
plt.title('x1')
plt.plot(np.arange(-M/2, M/2), x1)
plt.axis([-M/2,M/2,0,1])

plt.subplot(3,2,3)
plt.title('x2')
plt.plot(np.arange(-M/2, M/2),x2)
plt.axis([-M/2,M/2,-1,1])

plt.subplot(3,2,5)
plt.title('abs(DFT(x1 x x2))')
plt.plot(np.arange(-N/2, N/2),mY1)
plt.axis([-N/2,N/2,-80,max(mY1)])

Y2 = np.convolve(fftshift(fft(x1, M)), fftshift(fft(x2, M)))
mY2 = 20 * np.log10(np.abs(Y2)) - 40
mX1 = 20 * np.log10(np.abs(fftshift(fft(x1, M)))/M)
mX2 = 20 * np.log10(np.abs(fftshift(fft(x2, M)))/M)

plt.subplot(3,2,2)
plt.title('abs(DFT(x1))')
plt.plot(np.arange(-N/2, N/2),mX1)
plt.axis([-N/2,N/2,-80,max(mX1)])

plt.subplot(3,2,4)
plt.title('abs(DFT(x2))')
plt.plot(np.arange(-N/2, N/2),mX2)
plt.axis([-N/2,N/2,-80,max(mX2)])

plt.subplot(3,2,6)
plt.title('abs(DFT(x1) * DFT(x2))')
plt.plot(np.arange(-N/2, N/2),mY2[M/2:M+M/2])
plt.axis([-N/2,N/2,-80,max(mY2)])


plt.show()