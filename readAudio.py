import wave, struct
from serial_dac import *


#waveFile = wave.open('u2_2.wav', 'r')
#waveFile = wave.open('zdenda.wav', 'r')
#waveFile = wave.open('ahoj_2.wav', 'r')
waveFile = wave.open('petr.wav', 'r')
#waveFile = wave.open('cajovna.wav', 'r')
    
length = waveFile.getnframes()
#getnchannels
#getsampwidth
#getframerate

print(waveFile.getparams())
fs = waveFile.getframerate()


t = 0
x = 1
y = 1

oldSample = 0
inputData = 0

# Gain - multiplier for audio samples
gain = 5

#Skip X seconds
skipSeconds = 0

for i in range(0, skipSeconds  * fs):
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)

for i in range(0,length - skipSeconds * fs):

    # Read data sample - 2 bytes in this case
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)
    sample = int(data[0])

    # Simple filter
    #inputData = (sample + oldSample) / 2
    K = 0
    inputData = K * inputData + (1 - K) * sample

    # Detection of min/max values - DOES NOT WORK
    #x = min(x, data[0]) # min value
    #y = max(y, data[0]) # max value
    ##x = 0.99 * x + 0.01 * data[0]
    ##y = 0.99 * y + 0.01 * data[0]
    #print(x, y)

    #valueRelative = (((inputData * 200) + x) * 1000) / y
    valueRelative = (((inputData * gain) + 0x8000) * levelRelativeMax) / 0x7FFF
    oldSample = sample
    
    if valueRelative  < 0:
        valueRelative  = 0
    
    if valueRelative > levelRelativeMax:
        valueRelative  = levelRelativeMax

    period = dither(valueRelative)
    
    if t == 0:
        print("prefered Fs = ", 1/period)

    t = t + period
