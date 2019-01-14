import serial
import time
import math

#speed = 115200
speed = 1152000
#speed = 1000000

s = serial.Serial("/dev/ttyUSB0", speed)

timeToByte = speed / 9 # TODO 9 or 10?

#levelValues = [ (1 << i) - 1 for i in range(9)]

levelValues = [ 0x00, 0x08, 0x24, 0x92, 0xAA, 0xAE, 0xEE, 0xEF, 0xFF]

levelsProcentage = [(i) * 1000 / (len(levelValues) - 1) for i in range(len(levelValues))]




def mix(a,b):
    
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


#exit(1)




print(levelValues)
print(levelsProcentage)
print(len(levelValues))
print(len(levelsProcentage))



def setLevel(index):
#for i in range(8):
    value = levelValues[index]
    print(hex(value))
    print("{0:b}".format(value))
    for j in range(100):
        data = bytes((value,)) * 100
        s.write(data)
    #time.sleep(1)


def setValueInPercent(value):
    (min, max) = getRange(value)
    value = levelValues[index]
    print(hex(value))
    print("{0:b}".format(value))
    for j in range(100):
        data = bytes((value,)) * 100
        s.write(data)


#while 1:
#    s.write(b"\x00")


#    value = 75
#    min = 50 -> 0%
#    max = 100-> 100%

#    offset = value - min
#    range = (100 - 50) 
#    result = offset / range * 100

#duty cycle = 75
#0 10


#for i in range(9):
#    setLevel(i)
    
def findRange(value):
    #print("value", value)

    minValue = levelsProcentage[0]

    for i in range(len(levelsProcentage) - 1):
        #print("percentage", levelsProcentage[i])
        if value >= levelsProcentage[i]:
            minValue = levelsProcentage[i]
            if value <= levelsProcentage[i + 1]:
                maxValue = levelsProcentage[i + 1]

    return (minValue, maxValue)


def dither(value, numberOfBytes = 11):
    if (value < 0) or (value > 1000):
        print("Invalid value - must be in range 0 - 100%")
        return

    (minValue, maxValue) = findRange(value)

    offset = value - minValue
    valueRange = maxValue - minValue
    
    result = offset / valueRange
    
    #numberOfBytes = 7# #11 # TODO Make this configurable
    
    x = int(result * numberOfBytes)
    y = numberOfBytes - x


    minByte = bytes((levelValues[levelsProcentage.index(minValue)],))
    maxByte = bytes((levelValues[levelsProcentage.index(maxValue)],))


    array = mix(y * minByte, x * maxByte)
    #print(array)
    
    
    # TODO Remove following array - used only for debug
    arrayTest = mix(y * [minValue], x * [maxValue])
    mean = sum(arrayTest) / len(arrayTest)
    #print("Value: ", value, ", mean value: ", mean)

    loopCount = 1# TODO Make this configurable

    sendTime = numberOfBytes * 10 * loopCount / speed

    for i in range(loopCount):
        s.write(array)

    #print(sendTime)

    return sendTime

    #print("Min", minValue, "Max", maxValue)
    

if __name__ == "__main__":

    print("Tralala")

    #while 1:
    #    for i in range(10):
    #       dither(i*10)
            #dither(100)

    f = 1000
    t = 0
    oldTime = 0
    cycle = 0
    increase = True
    numberOfBytes = 7
    
    oddCycle = False
    
    while 1:
        #for i in range(0, 360):
        value  = 1000 * (math.sin(2 * math.pi * f * t) + 1) / 2
            #print(value)
        t = t + dither(int(value), numberOfBytes)
        #print(t)
        

        #cycle += 1

        if (t - oldTime > 1):
            if (oddCycle):
                levelValues = [ (1 << i) - 1 for i in range(9)]
                oddCycle = False
            else:
                levelValues = [ 0x00, 0x08, 0x24, 0x92, 0xAA, 0xAE, 0xEE, 0xEF, 0xFF]
                #oddCycle = True

            oldTime = t
            #print(numberOfBytes)
            
 
 
            #numberOfBytes += 2
            
            
        if False:#(t - oldTime > 0.1):
            oldTime = t
            print(f)

            if f < 300:
                increase = True

            if f > 3000:
                increase = False

            #cycle = 0
            
            if increase:
                f += 1
            else:
                f -= 1

        
        #f = int(100*t)
        #if (t % 2) > 1:
        #    print ("ted")

    

#def 

    


#    value = 75
#    min = 50 -> 0%
#    max = 100-> 100%

#    offset = value - min
#    range = (100 - 50) 
#    result = offset / range * 100

#duty cycle = 75
#0 10
