


import scipy.signal as signal
import matplotlib.pyplot as plt 
import numpy as np 

# lowpass = 10
lowpass = 20
xaxis = np.arange(lowpass) - (lowpass-1)/2
boxcar_window = signal.windows.boxcar(lowpass)
a = np.sum(abs(xaxis)*boxcar_window) / np.sum(abs(boxcar_window)) 
# a = 5.0

lowpass = 35
xaxis = np.arange(lowpass) - (lowpass-1)/2
hann_window = signal.windows.hann(lowpass)
b = np.sum(abs(xaxis)*hann_window) / np.sum(abs(hann_window))
# b = 5.0452

print ()
print ()
print (a)
print (b)

