# imports
import re
import os.path
import time
import math
#

def getCodes():
    while not os.path.exists("fil"):
        time.sleep(1)
    fil = open("fil", "r")
    rawRawText = fil.read()
    rawText = rawRawText.split("\n")
    codesList = []

    for line in rawText[4:-2]:
        codesLib = {}

        i = line.find(", pos=")
        n = line.rfind(",")
        codesLib["code"] = int(line[len("topcode="):i])

        x = int(line[i+len(", pos=")+1:n])
        y = int(line[n+1:-1])
        codesLib["pos"] = (x, y)
        codesList.append(codesLib)

    codes = getSeq(codesList)
    return codes

def getSeq(lib):
    "Control exc. sequence"
    startCode = 93
    startPos = (0,0)
    stopCode = 681
    stopPos = (0,0)
    codes = []

    for sublib in lib:
        if sublib["code"] == startCode:
            startPos = sublib["pos"]
            lib.remove(sublib)
        
        elif sublib["code"] == stopCode:
            stopPos = sublib["pos"]

    xDiff = (stopPos[0]- startPos[0])
    yDiff = (stopPos[1] - startPos[1])
    dirVector = (int(xDiff), int(yDiff))
    dirVectorLength = math.sqrt(dirVector[0]**2 + dirVector[1]**2)
    dirVector = (dirVector[0]/dirVectorLength , dirVector[1]/dirVectorLength)

    if dirVector == (0,0):
        # Didnt find start and stop
        return -1

    n = 10
    linePos = startPos
    finished = False
    while not finished:
        codeArea = [(linePos[0]-40, linePos[1]-40) , (linePos[0]+40, linePos[1]+40)]
        for sublib in lib:
            code = sublib["code"]
            pos = sublib["pos"]
            if (codeArea[0][0]<=pos[0]<=codeArea[1][0]) and (codeArea[0][1]<=pos[1]<=codeArea[1][1]):
                if code == stopCode:
                    finished = True
                    break  
                codes.append(code)
                lib.remove(sublib)
        linePos = ((linePos[0]+n*dirVector[0]), (linePos[1]+n*dirVector[1]))
        if (linePos[0] > stopPos[0]) or (linePos[1] > stopPos[1]):
            finished = True
                    
    if codes == []:
        return -1

    return codes
