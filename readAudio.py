import wave, struct

from serial_dac import *

voice = False

if voice:
    waveFile = wave.open('oh-yeah-everything-is-fine.wav', 'r')
else:
    #waveFile = wave.open('sound5.wav', 'r')
    #waveFile = wave.open('u2_2.wav', 'r')
    #waveFile = wave.open('zdenda.wav', 'r')
    #waveFile = wave.open('ahoj_2.wav', 'r')
    waveFile = wave.open('petr.wav', 'r')
    waveFile = wave.open('cajovna.wav', 'r')
    

length = waveFile.getnframes()
#getnchannels
#getsampwidth
#getframerate

print(waveFile.getparams())

fs = waveFile.getframerate()

#exit(1)

t = 0

x = 1
y = 1

oldSample = 0
inputData = 0

#Skip X seconds
skipSeconds = 0
for i in range(0, skipSeconds  * fs):
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)

for i in range(0,length - skipSeconds * fs):
    if voice:
        waveData = waveFile.readframes(1)
        data = struct.unpack("<2h", waveData)
        waveData = waveFile.readframes(1)
        data = struct.unpack("<2h", waveData)
        valuePercent = (((data[0]*5) + 10334) * 100) / 18125
        #print(data[0])
    else:
        waveData = waveFile.readframes(1)
        data = struct.unpack("<h", waveData)


        sample = int(data[0])
        #inputData = (sample + oldSample) / 2
        K = 0
        inputData = K * inputData + (1 - K) * sample

        #x = min(x, data[0]) # min value
        #y = max(y, data[0]) # max value
        
        #x = 0.99 * x + 0.01 * data[0]
        #y = 0.99 * y + 0.01 * data[0]

        #print(x, y)

        #valuePercent = (((inputData * 200) + x) * 1000) / y
        valuePercent = (((inputData * 5) + 0x8000) * 1000) / 0x7FFF
        oldSample = sample
    

    if valuePercent  < 0:
        valuePercent  = 0
    
    if valuePercent > 1000:
        valuePercent  = 1000

    #print(valuePercent)
    #for i in range(0, 360):
    #value  = 100 * (math.sin(2 * math.pi * f * t) + 1) / 2
            #print(value)
    
    period = dither(valuePercent)
    
    if t == 0:
        print("prefered Fs = ", 1/period)

    t = t + period
    
    
    
    #print(int(data[0]))
