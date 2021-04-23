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
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "10": [],
    "11": [],
    "12": [],
    "13": [],
    "14": [],
    "15": [],
    "16": [],
    "17": [],
    "18": [],
    "19": [],
    "20": []
}

stats = 0
sizeofTest = 5

print("""
### Test topcodes libary ###
This test is conducted to establish how spotcodes have to behave in picture for topcodes to read them correctly
Currently the max diameter of the spotcodes in topcodes is set to 300 pixels,
this.scanner.setMaxCodeDiameter(300)

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