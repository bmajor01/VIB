import sys, os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn import preprocessing
from numpy.fft import fft, ifft

wdir = r"G:\Measurements\241112_RezgesSzakdoga\241406_Tesztpad\measurements\rezgesterjedes_result"

files = os.listdir(wdir)

speed = []
CH1Vibs = []
CH2Vibs = []
CH3Vibs = []

for file in files:

    propfile = np.load(os.path.join(wdir,file))
    speed.append(propfile['arr_0'])
    CH1Vibs.append(propfile['arr_1'])
    CH2Vibs.append(propfile['arr_2'])
    CH3Vibs.append(propfile['arr_3'])

print(speed)

for location in range(len(speed)):
    print(location)
    plt.subplot(4,3,1+location)
    plt.title(speed[location])
    plt.imshow(CH1Vibs[::][location],aspect='auto',cmap='jet')
    plt.subplot(4,3,2+location)
    plt.imshow(CH2Vibs[::][location],aspect='auto',cmap='jet')
    plt.subplot(4,3,3+location)
    plt.imshow(CH3Vibs[::][location],aspect='auto',cmap='jet')
plt.show()