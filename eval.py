import sys, os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn import preprocessing
from numpy.fft import fft, ifft

wdir = r"G:\Measurements\241112_RezgesSzakdoga\241406_Tesztpad\measurements\devicetester_measurements\mot_8_dricer_1\M"

files = os.listdir(wdir)

speeds = []
torques = []
currents = []

asdsf = []

for file in files:
    ftype = file.split('_')
    measmode = ftype[0]
    ftype = ftype[1]
    ftype = ftype.split('.')
    ftype = ftype[0]

    if ftype == "dyn":
        dynfile = np.load(os.path.join(wdir,file))
        torque = dynfile['arr_0']
        speed = dynfile['arr_1']
        power = dynfile['arr_2']
        _current = dynfile['arr_3']

        _current = _current*2
        torque = torque * 0.001
        speed = speed * 0.1

        index = 25

        try:
            asdsf.append(torque[index])
            cim = _current[index]
        except:
            asdsf.append(0)

        avgspeed = np.mean(speed)

        speeds.append(np.max(speed))
        torques.append(np.max(torque))

        plt.plot(_current,torque)
        plt.title(str(str(round(avgspeed,1)) + " rpm"))
        plt.show()

        plt.plot(torque)
        plt.plot(speed)
        plt.plot(power)
        plt.plot(_current)
        plt.title(measmode)
        plt.show()

    else:

        dyn = file.split('_')
        dyn = str(dyn[0]+"_dyn.npz")
        dynfile = np.load(os.path.join(wdir,dyn))
        torque = dynfile['arr_0']
        speed = dynfile['arr_1']
        power = dynfile['arr_2']
        _current = dynfile['arr_3']

        _current = _current*2
        torque = torque * 0.001
        speed = speed * 0.1

        freq = np.linspace(1000,0,9)

        speed_low = int(np.min(speed) / 60)
        speed_high = int(np.max(speed) / 60)

        vibfile = np.load(os.path.join(wdir,file))

        CH1 = vibfile['arr_0']
        CH2 = vibfile['arr_1']
        CH3 = vibfile['arr_2']

        CH1 = CH1[:,:1000]
        CH1 = np.log10(CH1 + 1e-12)
        CH2 = CH2[:,:1000]
        CH2 = np.log10(CH2 + 1e-12)
        CH3 = CH3[:,:1000]
        CH3 = np.log10(CH3 + 1e-12)

        thresh = 0
        lpf = 50

        mask = np.arange(speed_low,speed_high)

        CH1[:,mask] = thresh
        CH2[:,mask] = thresh
        CH3[:,mask] = thresh

        #- értékeket eldobjuk
        CH1[CH1 < thresh] = thresh
        CH1[:,50] = thresh
        # CH1[:,150] = thresh
        # CH1[:,250] = thresh
        # CH1[:,300] = thresh
        # CH1[:,350] = thresh
        CH1[:,0] = thresh



        CH1_lowpass = CH1[:,:lpf]

        CH2[CH2 < thresh] = thresh
        CH2[:,50] = thresh
        # CH2[:,150] = thresh
        # CH2[:,250] = thresh
        # CH2[:,300] = thresh
        # CH2[:,350] = thresh
        CH2[:,0] = thresh

        CH2_lowpass = CH2[:,:lpf]

        CH3[CH3 < thresh] = thresh
        CH3[:,50] = thresh
        # CH3[:,150] = thresh
        # CH3[:,250] = thresh
        # CH3[:,300] = thresh
        # CH3[:,350] = thresh
        CH3[:,0] = thresh

        CH3_lowpass = CH3[:,:lpf]

        
        # CH1_lowpass = np.flip(CH1_lowpass.T)
        # CH2_lowpass = np.flip(CH2_lowpass.T)
        # CH3_lowpass = np.flip(CH3_lowpass.T)

        CH1_Power = np.mean(CH1_lowpass,axis=1)
        CH2_Power = np.mean(CH2_lowpass,axis=1)
        CH3_Power = np.mean(CH3_lowpass,axis=1)

        # plt.plot(CH1_Power)
        # plt.plot(CH2_Power)
        # plt.plot(CH3_Power)
        # plt.show()

        # CH1 = np.flip(CH1.T)
        # CH2 = np.flip(CH2.T)
        # CH3 = np.flip(CH3.T)

        CH1 = CH1.T
        CH2 = CH2.T
        CH3 = CH3.T

        # graph, plot = plt.subplots(2,3)

        plt.subplot(2,3,1)
        #plt.gca().set(ylim=(1,CH1.shape[0]))
        #plt.imshow(CH1,aspect='auto',cmap='jet',interpolation='none')
        plt.imshow(CH1,aspect='auto',cmap='jet')
        #plt.yticks(freq)
        #plt.xticks(torque)
        plt.title(measmode)
        #plt.colorbar()
        
        plt.subplot(2,3,2)
        #plt.imshow(CH2,aspect='auto',cmap='jet',interpolation='none')
        plt.imshow(CH2,aspect='auto',cmap='jet')
        
        plt.title(measmode)
        #plt.colorbar()

        plt.subplot(2,3,3)
        #plt.imshow(CH3,aspect='auto',cmap='jet',interpolation='none')
        plt.imshow(CH3,aspect='auto',cmap='jet')
        
        plt.title(measmode)
        #plt.colorbar()

        plt.subplot(2,3,4)
        plt.plot(CH1_Power)
        plt.xlim(0,len(CH1_Power))
        plt.subplot(2,3,5)
        plt.plot(CH2_Power)
        plt.xlim(0,len(CH2_Power))
        plt.subplot(2,3,6)
        plt.plot(CH3_Power)
        plt.xlim(0,len(CH3_Power))

        plt.show()

plt.plot(speeds, torques, 'rx')
#plt.plot(speeds,asdsf, 'rx')
plt.title(str(str(cim) + ' A'))
plt.show()