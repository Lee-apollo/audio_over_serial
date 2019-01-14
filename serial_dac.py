import serial
import time
import math

#speed = 115200
speed = 1152000
#speed = 1000000

s = serial.Serial("/dev/ttyUSB0", speed)

# Generated values with increasing mean value
#levelValues = [ (1 << i) - 1 for i in range(9)]

# Different version - precalculated values with a better distribution of ones and zeros
levelValues = [ 0x00, 0x08, 0x24, 0x92, 0xAA, 0xAE, 0xEE, 0xEF, 0xFF]

levelRelativeMax = 100

levelsRelative = [(i) * levelRelativeMax / (len(levelValues) - 1) for i in range(len(levelValues))]

def mix(a,b):
    
    return a + b
    
    # TODO Fix this function - it should be better
    bIndex = 0
    aIndex = 0

    try:
    
        c = [0] * (len(a) + len(b))
        x = (len(a) + len(b)) / 2
        for i in range(len(c)):
            if ((i % x) < len(a) / 2):
                #print("a", aIndex)
                c[i] = a[aIndex]
                aIndex += 1
            else:
                #print("b", bIndex)
                c[i] = b[bIndex]
                bIndex += 1
        return c
    except:
        print(len(a))
        print(aIndex)
        print(len(b))
        print(bIndex)

    #b = 3 * ["A"]
    #a = 2 * ["B"]

#print(mix(30 * ["0"], 5 * ["1"]))


def showLevels():
    print("Number of levels: ", len(levelValues))
    for i in range(len(levelValues)):
        print("Absolut value: {0:8b}, relative value: {1}".format(levelValues[i], levelsRelative[i]))
        
   
def findRange(value):
    #print("value", value)

    minValue = levelsRelative[0]

    for i in range(len(levelsRelative) - 1):
        #print("percentage", levelsRelative[i])
        if value >= levelsRelative[i]:
            minValue = levelsRelative[i]
            if value <= levelsRelative[i + 1]:
                maxValue = levelsRelative[i + 1]

    return (minValue, maxValue)


def dither(value, numberOfBytes = 11):
    if (value < 0) or (value > levelRelativeMax ):
        print("Invalid value - must be in range 0 - ", levelRelativeMax)
        return

    (minValue, maxValue) = findRange(value)

    offset = value - minValue
    valueRange = maxValue - minValue
    
    result = offset / valueRange
    
    numberOfHighBytes = int(result * numberOfBytes)
    numberOfLowBytes = numberOfBytes - numberOfHighBytes


    minByte = bytes((levelValues[levelsRelative.index(minValue)],))
    maxByte = bytes((levelValues[levelsRelative.index(maxValue)],))

    array = mix(numberOfLowBytes * minByte, numberOfHighBytes * maxByte)
    
    # TODO Remove following array - used only for debug
    arrayTest = mix(numberOfLowBytes * [minValue], numberOfHighBytes * [maxValue])
    mean = sum(arrayTest) / len(arrayTest)
    #print("Value: ", value, ", mean value: ", mean)

    loopCount = 1# TODO Make this configurable

    # Calculate time needed for sending of this sample, 10 represents 8 bits + 1 start bit + 1 stop bit TODO Maybe there are 2 stop bits. Check it.
    sendTime = numberOfBytes * 10 * loopCount / speed

    for i in range(loopCount):
        s.write(array)

    return sendTime


showLevels()

if __name__ == "__main__":



    #while 1:
    #    for i in range(10):
    #       dither(i*10)
            #dither(100)

    f = 1000
    t = 0
    oldTime = 0
    cycle = 0
    increase = True
    
    while 1:
        #for i in range(0, 360):
        value  = levelRelativeMax * (math.sin(2 * math.pi * f * t) + 1) / 2
        t = t + dither(int(value))

        if (t - oldTime > 0.1):
            oldTime = t
            print(f)

            if f < 300:
                increase = True

            if f > 3000:
                increase = False

            if increase:
                f += 1
            else:
                f -= 1
