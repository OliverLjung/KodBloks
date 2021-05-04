import os
from getPic import getCodesForImage

### CHEAT ###

startCode = 93
stopCode = 681

moveForward = 87
turnRight = 79
turnLeft = 61

whileStartCode = 47
endCode = 55
ifStartCode =  59
elseStartCode = 103


pathAheadCode = 109
pathLeftCode = 115
pathRightCode = 117
notFinishedCode = 121

#############

expectedResult = {
    "1": [startCode, moveForward, turnRight, moveForward, turnLeft, stopCode],
    "2": [startCode, whileStartCode, notFinishedCode, moveForward, turnRight, moveForward, turnLeft, endCode, stopCode],
    "3": [startCode, whileStartCode, pathAheadCode, moveForward, endCode, stopCode],
    "4": [startCode, whileStartCode, pathAheadCode, moveForward, endCode, stopCode],
    "5": [startCode, ifStartCode, pathRightCode, moveForward, endCode, elseStartCode,turnLeft, endCode,stopCode],
    "6": [ifStartCode, turnLeft, endCode, whileStartCode, pathRightCode, stopCode, startCode],
    "7": [ifStartCode, whileStartCode, pathRightCode, stopCode],
    "8": [endCode, endCode, endCode, pathAheadCode, startCode],
    "9": [startCode, turnLeft, endCode, endCode, elseStartCode],
    "10": [turnLeft, ifStartCode, moveForward, pathAheadCode, startCode],
    "11": [whileStartCode, turnLeft, ifStartCode, moveForward, pathAheadCode, notFinishedCode, startCode],
    "12": [endCode, endCode, endCode, stopCode],
    "13": [notFinishedCode, endCode, endCode, endCode, stopCode, startCode, pathAheadCode],
    "14": [notFinishedCode, endCode, endCode, endCode, stopCode, startCode, pathAheadCode],
    "15": [notFinishedCode, ifStartCode, endCode, endCode, endCode, stopCode, startCode, whileStartCode, pathAheadCode, moveForward, turnLeft],
    "16": [notFinishedCode, ifStartCode, startCode, whileStartCode, pathAheadCode, moveForward, turnLeft],
    "17": [notFinishedCode, ifStartCode, startCode, stopCode, whileStartCode, pathAheadCode, moveForward, turnLeft],
    "18": [notFinishedCode, turnRight, ifStartCode, startCode, stopCode, whileStartCode, pathRightCode, pathAheadCode, moveForward, turnLeft],
    "19": [turnRight, ifStartCode, stopCode, pathRightCode, whileStartCode, pathAheadCode],
    "20": [stopCode, startCode]
}

stats = 0
sizeofTest = 20

print("""
### Test topcodes libary ###
This test is conducted to establish how spotcodes have to behave in picture for topcodes to read them correctly
Currently the max diameter of the spotcodes in topcodes is set to 100 pixels,
this.scanner.setMaxCodeDiameter(100)

""")

for nr in range(1,sizeofTest+1):
    bildname = f"pics/bild{nr}.jpg"
    os.rename(bildname,"bild.jpg")
    thisExpected = expectedResult[f"{nr}"]
    # Run test
    os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
    thisResult = getCodesForImage()
    thisExpected.sort()
    thisResult.sort()

    if thisExpected == thisResult:
        r = "Passed"
        stats += 1
    else:
        r = "Failed"
    
    print(f"Test{nr}: {r}")
    # 
    os.rename("bild.jpg", bildname)

print(f"\nProcentage passed: {stats/sizeofTest * 100}%")