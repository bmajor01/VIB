import sys, os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn import preprocessing
from numpy.fft import fft, ifft
from pybaselines import Baseline, utils


wdir = r"G:\Measurements\241112_RezgesSzakdoga\241406_Tesztpad\measurements\RezgesTerjedesResult01"

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

# minvalue = -12
# maxvalue = 10

#fig, axs = plt.subplots(nrows = 4, ncols = 3, figsize=(15, 6), facecolor='w', edgecolor='k')


fig = plt.figure(figsize=(8, 8))

columns = 1
rows = 3

fig = plt.figure(figsize=(8, 8))


for location in range(1, columns*rows +1):

    # arr = CH3Vibs[location][0]
    speedIndex = 2

    #allCH = CH1Vibs + CH2Vibs + CH3Vibs

    #allCH = np.sum(allCH,1)

    baseline_fitter = Baseline(x_data= freq)

    y = CH2Vibs[location][speedIndex]

    bkg_1, params_1 = baseline_fitter.modpoly(y, poly_order=3)
    bkg_2, params_2 = baseline_fitter.asls(y, lam=1e7, p=0.04)
    bkg_3, params_3 = baseline_fitter.mor(y, half_window=100)
    bkg_4, params_4 = baseline_fitter.snip(y, max_half_window=40, decreasing=True, smooth_half_window=3)




    fig.add_subplot(rows, columns, location)
    #plt.plot(freq,CH2Vibs[location][speedIndex])
    plt.xlim(0,1000)
    plt.ylim(-20,20)

    #plt.plot(freq, bkg_1, '--', label='modpoly')
    plt.plot(freq, bkg_2, '--', label='asls')
    #plt.plot(freq, bkg_3, '--', label='mor')
    #plt.plot(freq, bkg_4, '--', label='snip')

    #plt.plot(freq,avg[location])
    #plt.imshow(CH3Vibs[location],aspect='auto',cmap='jet',interpolation='nearest',vmin=minvalue, vmax=maxvalue)
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