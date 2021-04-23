# imports
from var import Config
from camera import Camera
# for getting codes
import re
import os
import time
import math
# for getting picture
import numpy as np
import cv2
import threading
## alt
import pygame
import pygame.camera
from pygame.locals import *
pygame.init()

triedFlip = False

# camSize = (1280, 720)
# pygame.camera.init()
# camlist = pygame.camera.list_cameras()
# if camlist:
#     cam = pygame.camera.Camera(camlist[0], camSize)
#     cam.start()
#     image = cam.get_image()
# else:
#     print("Error in camera")
#     game.stopGame()


threadLock = threading.Lock()


t0 = 0

def buttonsImage():
    # BUTTONPOS = [(minX, minY), (maxX, maxY)]
    HELPBUTTONPOS = [(0,0), (0,0)]
    HELPBUTTONCODE = 0
    RUNBUTTONPOS = [(0,0), (0,0)]
    RUNBUTTONCODE = 0

    os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")

    codesLib = getCodesForImage()
    for lib in codesLib:
        if lib["code"] == HELPBUTTONCODE:
            if (HELPBUTTONPOS[0][0] <= lib["pos"][0] <= HELPBUTTONPOS[1][0]) and (HELPBUTTONPOS[0][1] <= lib["pos"][1] <= HELPBUTTONPOS[1][1]):
                return "help"

        elif lib["code"] == RUNBUTTONCODE:
            if (RUNBUTTONPOS[0][0] <= lib["pos"][0] <= RUNBUTTONPOS[1][0]) and (RUNBUTTONPOS[0][1] <= lib["pos"][1] <= RUNBUTTONPOS[1][1]):
                return "run"

    
    getPicFlip()
    os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
    
    codesLib = getCodesForImage()
    for lib in codesLib:
        if lib["code"] == HELPBUTTONCODE:
            if (HELPBUTTONPOS[0][0] <= lib["pos"][0] <= HELPBUTTONPOS[1][0]) and (HELPBUTTONPOS[0][1] <= lib["pos"][1] <= HELPBUTTONPOS[1][1]):
                return "help"

        elif lib["code"] == RUNBUTTONCODE:
            if (RUNBUTTONPOS[0][0] <= lib["pos"][0] <= RUNBUTTONPOS[1][0]) and (RUNBUTTONPOS[0][1] <= lib["pos"][1] <= RUNBUTTONPOS[1][1]):
                return "run"

    return None
            

def getCodesForImage():
    while not os.path.exists("fil"):
        time.sleep(0.1)
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
    return codesList

def getPicFlip():
    image = pygame.image.load("bild.jpg")
    image = pygame.transform.flip(image, True, True)
    image = pygame.transform.scale(image, (1920, 1080))
    pygame.image.save(image, "bild.jpg")

def getPic():
    global threadLock
    global triedFlip
    triedFlip = False

    Camera.haltSetter(True)
    while Camera.picReady is False:
        time.sleep(0.1)
    image = cv2.imread("bildSRC.jpg")
    cv2.imwrite("bild.jpg", image)
    Camera.haltSetter(False) 
        
def getCodes():
    global t0
    t0 = time.time()
    while not os.path.exists("fil"):
        time.sleep(0.1)
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
    global t0

    startCode = 93
    startPos = (0,0)
    stopCode = 681
    stopPos = (0,0)

    whileStartCode = 47
    endCode = 55
    ifStartCode =  59
    elseStartCode = 103

    iterations = [whileStartCode, ifStartCode]

    pathAheadCode = 109
    pathLeftCode = 115
    pathRightCode = 117
    notFinishedCode = 121

    RUNBUTTONCODE = 0
    HELPBUTTONCODE = 0

    conditions = [pathAheadCode, pathLeftCode, pathRightCode, notFinishedCode]

    codes = []
    stopCodeFound = False
    startCodeFound = False

    for sublib in lib:
        if sublib["code"] == startCode:
            startPos = sublib["pos"]
            lib.remove(sublib)
            startCodeFound = True
        
        elif sublib["code"] == stopCode:
            stopPos = sublib["pos"]
            stoplib = sublib
            stopCodeFound = True

    if not(startCodeFound and stopCodeFound):
        return -1

    lib.remove(stoplib)
    lib.append(stoplib)

    xDiff = (stopPos[0]- startPos[0])
    yDiff = (stopPos[1] - startPos[1])
    dirVector = (xDiff, yDiff)
    dirVectorLength = math.sqrt(dirVector[0]**2 + dirVector[1]**2)

    if dirVectorLength == 0:
        # Didnt find start and stop
        return -1

    dirVector = (dirVector[0]/dirVectorLength , dirVector[1]/dirVectorLength)

    if dirVector == (0,0):
        # Didnt find start and stop
        return -1

    n = 5
    linePos = startPos
    searchForCond = False
    condVector = (-dirVector[1], dirVector[0])
    finished = False
    codeArea = [startPos,startPos]

    while not finished:
        if 10 < (time.time() - t0):
            print("Stuck in loop")
            game.stopGame()

        for sublib in lib:
            code = sublib["code"]
            pos = sublib["pos"]
            if (code == RUNBUTTONCODE) or (code == HELPBUTTONCODE):
                lib.remove(sublib)
                continue

            if (codeArea[0][0]<=pos[0]<=codeArea[1][0]) and (codeArea[0][1]<=pos[1]<=codeArea[1][1]):
                if searchForCond:
                    if code in conditions:
                        codes.append((code, pos))
                        lib.remove(sublib)
                        searchForCond = False
                else:
                    if code == stopCode:
                        finished = True
                        break
                    elif code in iterations:
                        codes.append((code, pos))
                        lib.remove(sublib)
                        searchForCond = True
                        postemp = pos
                        linePosCond = pos
                    else:
                        codes.append((code, pos))
                        lib.remove(sublib)

        if searchForCond:
            linePosCond = ((linePosCond[0]+n*condVector[0]), (linePosCond[1]+n*condVector[1]))
            codeArea = [(linePosCond[0]-50, linePosCond[1]-50) , (linePosCond[0]+50, linePosCond[1]+50)]
            if (linePosCond[0] > stopPos[0]+500*condVector[0]) and (linePosCond[1] > stopPos[1]+500*condVector[0]):
                return -2
        else:
            linePos = ((linePos[0]+n*dirVector[0]), (linePos[1]+n*dirVector[1]))
            codeArea = [(linePos[0]-50, linePos[1]-50) , (linePos[0]+50, linePos[1]+50)]
            if (linePos[0] > stopPos[0]) and (linePos[1] > stopPos[1]):
                finished = True
                    
    if codes == []:
        return -1

    codes.reverse()

    array = getListSeq(codes, [])

    return array


def getListSeq(codes, array):

    if codes == []:
        return []

    whileStartCode = 47
    endCode = 55
    ifStartCode =  59
    elseStartCode = 103

    iterations = [whileStartCode, ifStartCode, elseStartCode]

    pathAheadCode = 109
    pathLeftCode = 115
    pathRightCode = 117
    notFinishedCode = 121

    conditions = [pathAheadCode, pathLeftCode, pathRightCode, notFinishedCode]

    thisList = []

    info = codes.pop()
    code = info[0]
    pos = info[1]


    if code == endCode:
        return array
    elif code == whileStartCode:
        thisList.append(code)
        info = codes.pop()
        code = info[0]
        pos = info[1]
        if code not in conditions:
            game.stopGame()
        else:
            thisList.append(code)
            thisList.append(getListSeq(codes, thisList))
            return [thisList] + getListSeq(codes, thisList)
    elif code == ifStartCode:
        thisList.append(code)
        info = codes.pop()
        code = info[0]
        pos = info[1]
        if code not in conditions:
            game.stopGame()
        else:
            thisList.append(code)
            thisList.append(getListSeq(codes, thisList))
            return [thisList] + getListSeq(codes, thisList)
    elif code == elseStartCode:
        thisList.append(code)
        thisList.append(getListSeq(codes, thisList))
        return [thisList] + getListSeq(codes, [])
    else:
        return [[code]] + getListSeq(codes, [])

    
