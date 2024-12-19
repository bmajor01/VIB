import sys, os  # System and OS libraries for interacting with the file system
import numpy as np  # Library for numerical computations
import matplotlib.pyplot as plt  # Library for plotting
from numpy.fft import fft, ifft
from array import array

MeasFolders = r"G:\Measurements\241112_RezgesSzakdoga\241406_Tesztpad\measurements\TesztPadRezgésTerjedés"
Outdir = r"G:\Measurements\241112_RezgesSzakdoga\241406_Tesztpad\measurements\rezgesterjedes_result"

folders = os.listdir(MeasFolders)
#print(folders)

CH1Vibs = []
CH2Vibs = []
CH3Vibs = []

files = os.listdir(os.path.join(MeasFolders,folders[0]))

speeds = []
for file in files:
    fname = file.split("_")
    if fname[1] == "vib.npz":
        fnamestrs = fname[0].split(" ")
        speedstr = fnamestrs[1]
        speeds.append(int(speedstr[1::]))
#print(speeds)

for speed in speeds:

    fname = "G3 S"+ str(speed) +" A20_vib.npz"
    
    for folder in folders:

            # Load vibration data

        vibfile = np.load(os.path.join(MeasFolders,folder, fname))

        #print(folder, file)

        crop = 1000

        fftlength = 20000-crop
        sr = 2000

        freq = np.fft.fftfreq(fftlength,1/sr)

        window = np.hamming(fftlength)


        CH1 = np.array(vibfile['arr_0'])  # Channel 1 data
        CH2 = np.array(vibfile['arr_1'])  # Channel 2 data
        CH3 = np.array(vibfile['arr_2'])  # Channel 3 data

        CH1 = CH1[0]
        CH2 = CH2[0]
        CH3 = CH3[0]

        CH1_W = CH1[crop::] * window
        CH2_W = CH2[crop::] * window
        CH3_W = CH3[crop::] * window

            # plt.plot(CH1[crop::])
            # plt.plot(CH2[crop::])
            # plt.plot(CH3[crop::])
            # plt.show()

        CH1_FFT=abs(fft(CH1_W))
        CH2_FFT=abs(fft(CH2_W))
        CH3_FFT=abs(fft(CH3_W))

        CH1_FFT = 10*np.log10(CH1_FFT + 1e-12)
        CH2_FFT = 10*np.log10(CH2_FFT + 1e-12)
        CH3_FFT = 10*np.log10(CH3_FFT + 1e-12)

            # print(CH1_FFT)

        length = int(len(freq)/2)

            # plt.plot(freq[0:length],CH1_FFT[0:length])
            # plt.plot(freq[0:length],CH2_FFT[0:length])
            # plt.plot(freq[0:length],CH3_FFT[0:length])

        CH1Vibs.append(CH1_FFT[0:length])
        CH2Vibs.append(CH2_FFT[0:length])
        CH3Vibs.append(CH3_FFT[0:length])

            # plt.imshow(CH2,aspect='auto', cmap='jet')
            # plt.imshow(CH3,aspect='auto', cmap='jet')
        lastFolder = folder

        
    #outfile = file.split(".")

    print(os.path.join(Outdir, str("fft_" + str(speed) + ".npz")))

    np.savez((os.path.join(Outdir, str("fft_" + str(speed) + ".npz"))),speed,CH1Vibs,CH2Vibs,CH3Vibs)

    plt.imshow(CH1Vibs,aspect='auto',cmap='jet')
    plt.show()
# for samples in range(len(CH1Vibs)):
#     plt.plot(freq[0:length],CH1Vibs[samples])
#plt.imshow(CH1Vibs,aspect='auto',cmap='jet')
