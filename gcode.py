import serial
        
ser = serial.Serial('COM4', 115200)
print(ser.name)

file1 = open('GCode.txt', 'r')
Lines = file1.readlines()
linecounter = 0

ser.write(str.encode("G0"))
print(ser.readline())

while 1:
    ser.write(str.encode(Lines[linecounter]+ "\r\f"))
    print(str.encode(Lines[linecounter]))
    resp = ser.readline()
    print(Lines[linecounter])
    print(resp)
    linecounter += 1
    if Lines[linecounter] == 'Q':
        break
ser.close()             
print("End")