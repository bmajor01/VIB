import sys, os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn import preprocessing
from numpy.fft import fft, ifft


wdir = r"G:\Measurements\241112_RezgesSzakdoga\241406_Tesztpad\measurements\rezgesterjedes_result"

files = os.listdir(wdir)

locations = []
speed = []
CH1Vibs = []
CH2Vibs = []
CH3Vibs = []

all = []

for file in files:

    propfile = np.load(os.path.join(wdir,file))
    locations =     (propfile['arr_0'])
    speed.append    (propfile['arr_1'])
    CH1Vibs.append  (propfile['arr_2'])
    CH2Vibs.append  (propfile['arr_3'])
    CH3Vibs.append  (propfile['arr_4'])
    freq = (propfile['arr_5'])

all.append(CH1Vibs)
all.append(CH2Vibs)
all.append(CH3Vibs)

minvalue = np.min(all)
maxvalue = np.max(all)

minvalue = -12
maxvalue = 10

#fig, axs = plt.subplots(nrows = 4, ncols = 3, figsize=(15, 6), facecolor='w', edgecolor='k')


fig = plt.figure(figsize=(8, 8))

columns = 1
rows = 4

fig = plt.figure(figsize=(8, 8))

for location in range(1, columns*rows +1):

    # arr = CH3Vibs[location][0]
    speedIndex = 3

    fig.add_subplot(rows, columns, location)
    #plt.plot(freq,CH3Vibs[location][speedIndex])
    plt.imshow(CH3Vibs[location],aspect='auto',cmap='jet',vmin=minvalue, vmax=maxvalue)
    plt.title(locations[location-1] + " speed = " + str( speed[speedIndex]))

    # print(location)

    # plt.subplot(4,3,(1+location))
    # plt.title(str(locations[location]))
    # plt.imshow(CH1Vibs[location],aspect='auto',cmap='jet')

    # print(1+location)

    # plt.subplot(4,3,(2+location))
    # plt.title(str(locations[location]))
    # plt.imshow(CH2Vibs[location],aspect='auto',cmap='jet')

    # print(2+location)

    # plt.subplot(4,3,(3+location))
    # plt.title(str(locations[location]))
    # plt.imshow(CH3Vibs[location],aspect='auto',cmap='jet')

    # print(3+location)

    # plt.show()

    #print(location)
plt.show()