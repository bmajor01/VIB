import pyvisa as visa
import sys, os
import time
import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import minimalmodbus
import serial
import struct
from numpy.fft import fft, ifft

def meas():

    #Arduino serial init
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.5) 
    print("Rebooting Arduino...")
    time.sleep(1)

    print(SendGCode(arduino, "G0"))

    #MODBUS init
    instrument = minimalmodbus.Instrument('COM5',1)
    instrument.serial.port
    instrument.serial.baudrate = 19200
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.bytesize = 8
    instrument.serial.stopbits = 2
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.serial.timeout = 0.1

    #PyVISA INIT
    rm = visa.ResourceManager()
    instruments = rm.list_resources()
    usb = list(filter(lambda x: 'USB' in x, instruments))
    if len(usb) != 1:
        print('Bad instrument list', instruments)
        sys.exit(-1)

    psu = rm.open_resource(usb[0]) # bigger timeout for long mem

    #NI DAQMX INIT

    #MEASUREMENT LENGTH
    N = 2000
    #MEASUREMENT SAMPLE RATE
    sr = 2000

    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai2", terminal_config=TerminalConfiguration.RSE)
    task.timing.cfg_samp_clk_timing(rate=sr, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=N)

    #MEASUREMENT START

    acceleration = 30

    max_current = 3
    current_step_no = 20

    # 1/4 step oriental
    # min_rpm = 4000
    # max_rpm = 9000
    # step_rpm = 50

    #fullstep sanyo
    min_rpm = 500
    max_rpm = 2300
    step_rpm = 10

    print(psu.query('*IDN?'))
    
    currents = np.linspace(0,max_current,current_step_no)
    rpms = np.linspace(min_rpm, max_rpm, step_rpm)

    psu.write(':OUTPut:PAIR PARallel')

    time.sleep(2)

    for rpm in rpms:
        torque = []
        speed = []
        power = []

        CH1 = []
        CH2 = []
        CH3 = []

        _current = []

        _GCodeString = str("G3 S" + str(int(rpm)) + " A" + str(acceleration))

        WaitAcceleration(arduino, _GCodeString)

        psu.write(':OUTP CH1,ON')
        psu.write(':APPL CH1,30,0')
        time.sleep(2)

        for current in currents:
            psu.write(':APPL CH1,30,' + str(current))
            time.sleep(0.1)
            torque.append(registersToInt(instrument.read_registers(0,2)))
            speed.append(registersToInt(instrument.read_registers(2,2)))
            power.append(registersToInt(instrument.read_registers(4,2)))
            task.start()
            new_data = task.read(number_of_samples_per_channel=N)
            task.stop()
            #new_data = task.read()
            CH1.append(abs(fft(new_data[0])))
            CH2.append(abs(fft(new_data[1])))
            CH3.append(abs(fft(new_data[2])))
            _current.append(current)
            print(current)
            if registersToInt(instrument.read_registers(2,2)) < (np.mean(speed)*0.5):
                print("steploss")
                break

        psu.write(':OUTP CH1,OFF')
        SendGCode(arduino, "s")
    
        np.savez(str("G3 S" + str(int(rpm)) + " A20_vib.npz"),CH1,CH2,CH3)
        np.savez(str("G3 S" + str(int(rpm)) + " A20_dyn.npz"),torque,speed,power,_current)
        time.sleep(2)


    # plt.subplot(1,3,1)
    # plt.imshow(CH1[1::],aspect='auto')
    # plt.subplot(1,3,2)
    # plt.imshow(CH2[1::],aspect='auto')
    # plt.subplot(1,3,3)
    # plt.imshow(CH3[1::],aspect='auto')
    # plt.show()

    # np.savez("G3 S2000 A20 vib.npz",CH1,CH2,CH3)
    # np.savez("G3 S2000 A20 sensor.npz",torque,speed,power,_current)
    
    # plt.subplot(1,3,1)
    # plt.plot(CH1[1::],aspect='auto')
    # plt.subplot(1,3,2)
    # plt.plot(CH2[1::],aspect='auto')
    # plt.subplot(1,3,3)
    # plt.plot(CH3[1::],aspect='auto')
    # plt.show()

    # plt.plot(torque)
    # plt.plot(speed)
    # plt.plot(power)
    # plt.plot(_current)

    #plt.show()

def SendGCode(device, x): 
	_out = str(x + "\r\n")
	_str = bytes(_out, 'utf-8')
	device.write(_str) 
	time.sleep(0.1) 
	data = device.readline()  
	return data 

def WaitAcceleration(device, x):
    data = device.readline() 
    _out = str(x + "\r\n")
    _str = bytes(_out, 'utf-8')
    device.write(_str)
   
    while(data != b'AtMaxSpeed\r\n'):
        data = device.readline()  
        print(data)
    data = device.readline() 
    return 0

def registersToInt(_regVal):
    _hex = str("{:04x}".format(_regVal[0]) + "{:04x}".format(_regVal[1]))
    return(struct.unpack('>i', bytes.fromhex(_hex))[0])

def PetiregistersToInt(_regVal):
    #_hex = str("{:04x}".format(_regVal[0]) + "{:04x}".format(_regVal[1]))
    _hex = str(hex(_regVal[0])[2:].rjust(4, '0') + hex(_regVal[1])[2:].rjust(4, '0'))
    return(struct.unpack('>i', bytes.fromhex(_hex))[0])

def readTorque():

    instrument = minimalmodbus.Instrument('COM6',1)
    instrument.serial.port
    instrument.serial.baudrate = 19200
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.bytesize = 8
    instrument.serial.stopbits = 2
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.serial.timeout = 0.1

    torque = []
    speed = []
    power = []

    for k in range(100):
        print(k)
        torque.append(PetiregistersToInt(instrument.read_registers(0,2)))
        speed.append(PetiregistersToInt(instrument.read_registers(2,2)))
        power.append(PetiregistersToInt(instrument.read_registers(4,2)))

        #time.sleep(0.001)

    plt.plot(torque)
    plt.plot(speed)
    plt.plot(power)
    plt.show()

def dummy1():
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE)
    task.start()




    rm = visa.ResourceManager()
    # Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
    instruments = rm.list_resources()
    usb = list(filter(lambda x: 'USB' in x, instruments))
    if len(usb) != 1:
        print('Bad instrument list', instruments)
        sys.exit(-1)

    psu = rm.open_resource(usb[0]) # bigger timeout for long mem

    print(psu.query('*IDN?'))
    psu.write(':SYST:BRIG 100')

    #psu.write(':APPL CH1,5,0.01')

    #time.sleep(1)
    #print(psu.query(':MEAS:CURR? CH1'))
    #psu.write(':OUTP CH1,OFF')
    #psu.write(':SYST:BRIG 0')

    currents = np.linspace(0,3.2,100)

    psu.write(':OUTP CH1,ON')

    m_current = []
    m_power = []
    m_voltage = []
    m_torque = []



    for current in currents:
        psu.write(':APPL CH1,30,' + str(current))
        #psu.write(':APPL CH1,'+ str(current)+'1')
        time.sleep(0.01)
        m_torque.append(task.read(number_of_samples_per_channel=1))
        m_current.append(float(psu.query(':MEAS:CURR? CH1')))
        m_voltage.append(float(psu.query(':MEAS:VOLT? CH1')))
        m_power.append(float(psu.query(':MEAS:POWE? CH1')))

    psu.write(':OUTP CH1,OFF')

    np.savez("meas5.npz",m_torque,m_current,m_voltage,m_power)

    plt.plot(m_voltage)
    plt.plot(m_current)
    plt.plot(m_power)
    plt.plot(m_torque)
    plt.show()



    # psu.write(':SYST:BRIG 100')
    # psu.write(':SYST:BRIG 0')
    # psu.write(':SYST:BRIG 100')
    # psu.write(':APPL CH1,5,0.01')
    # psu.write(':OUTP CH1,ON')
    # time.sleep(1)


    # #print(psu.query(':MEAS? CH1'))
    # time.sleep(1)
    # psu.write(':OUTP CH1,OFF')

def _3dh():

    #MODBUS init
    instrument = minimalmodbus.Instrument('COM5',1)
    instrument.serial.port
    instrument.serial.baudrate = 19200
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.bytesize = 8
    instrument.serial.stopbits = 2
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.serial.timeout = 0.1

    #PyVISA INIT
    rm = visa.ResourceManager()
    instruments = rm.list_resources()
    usb = list(filter(lambda x: 'USB' in x, instruments))
    if len(usb) != 1:
        print('Bad instrument list', instruments)
        sys.exit(-1)

    psu = rm.open_resource(usb[0]) # bigger timeout for long mem

    #NI DAQMX INIT

    #MEASUREMENT LENGTH
    N = 2000
    #MEASUREMENT SAMPLE RATE
    sr = 2000

    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai2", terminal_config=TerminalConfiguration.RSE)
    task.timing.cfg_samp_clk_timing(rate=sr, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=N)

    #MEASUREMENT START

    max_current = 3
    current_step_no = 50

    # 1/4 step oriental
    # min_rpm = 4000
    # max_rpm = 9000
    # step_rpm = 50

    print(psu.query('*IDN?'))
    
    currents = np.linspace(0,max_current,current_step_no)

    psu.write(':OUTPut:PAIR PARallel')

    time.sleep(2)

    measurements = 1

    for rpm in np.arange(measurements):
        torque = []
        speed = []
        power = []

        CH1 = []
        CH2 = []
        CH3 = []

        _current = []

        psu.write(':OUTP CH1,ON')
        psu.write(':APPL CH1,30,0')
        time.sleep(2)

        for current in currents:
            psu.write(':APPL CH1,30,' + str(current))
            time.sleep(0.1)
            torque.append(registersToInt(instrument.read_registers(0,2)))
            speed.append(registersToInt(instrument.read_registers(2,2)))
            power.append(registersToInt(instrument.read_registers(4,2)))
            task.start()
            new_data = task.read(number_of_samples_per_channel=N)
            task.stop()
            #new_data = task.read()
            CH1.append(abs(fft(new_data[0])))
            CH2.append(abs(fft(new_data[1])))
            CH3.append(abs(fft(new_data[2])))
            _current.append(current)
            print(current)
            if registersToInt(instrument.read_registers(2,2)) < (np.mean(speed)*0.5):
                print("steploss")
                break

        psu.write(':OUTP CH1,OFF')
    
        np.savez(str("_3DH" + str(int(rpm)) + " _vib.npz"),CH1,CH2,CH3)
        np.savez(str("_3DH" + str(int(rpm)) + " _dyn.npz"),torque,speed,power,_current)
        time.sleep(2)

if __name__ == '__main__':
    #dummy1()
    #readTorque()
    #meas()
    _3dh()