# imports

# for getting codes
import re
import os.path
import time
import math
# for getting picture
import cv2
## alt
# import pygame
# import pygame.camera
# from pygame.locals import *
# pygame.init()
# pygame.camera.init()


def getPic():
    try:
        camera = cv2.VideoCapture(cv2.CAP_DSHOW)
        time.sleep(0.5)  # If you don't wait, the image will be dark
        check, image = camera.read()
        if check:
            cv2.imwrite("bild.jpg", image)
        else:
            raise(Exception)
        camera.release() 
    except Exception:
        print("Error in camera")
    
    #camlist = pygame.camera.list_cameras()
    # if camlist:
    #     cam = pygame.camera.Camera(camlist[0],(1280 , 720))
    #     cam.start()
    #     time.sleep(0.5)
    #     image = cam.get_image()
    #     pygame.image.save(image, "bild.jpg")

    # else:
    #     print("Error in camera")
    
def getCodes():
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

    conditions = [pathAheadCode, pathLeftCode, pathRightCode, notFinishedCode]

    codes = []

    for sublib in lib:
        if sublib["code"] == startCode:
            startPos = sublib["pos"]
            lib.remove(sublib)
        
        elif sublib["code"] == stopCode:
            stopPos = sublib["pos"]
            lib.remove(sublib)
            lib.append(sublib)

    xDiff = (stopPos[0]- startPos[0])
    yDiff = (stopPos[1] - startPos[1])
    dirVector = (xDiff, yDiff)
    dirVectorLength = math.sqrt(dirVector[0]**2 + dirVector[1]**2)

    if dirVectorLength == 0:
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
    codeArea = [(0,0),(0,0)]

    while not finished:
        for sublib in lib:
            code = sublib["code"]
            pos = sublib["pos"]

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
            debug("conditions", pos)
            raise SystemExit
        else:
            thisList.append(code)
            thisList.append(getListSeq(codes, thisList))
    elif code == ifStartCode:
        thisList.append(code)
        info = codes.pop()
        code = info[0]
        pos = info[1]
        if code not in conditions:
            debug("conditions", pos)
            raise SystemExit
        else:
            thisList.append(code)
            thisList.append(getListSeq(codes, thisList))
    elif code == elseStartCode:
        thisList.append(code)
        info = codes.pop()
        code = info[0]
        pos = info[1]
        if code not in conditions:
            debug("conditions", pos)
            raise SystemExit
        else:
            thisList.append(code)
            thisList.append(getListSeq(codes, thisList))
    else:
        return [[code]] + getListSeq(codes, [])

    return [thisList] + getListSeq(codes, thisList)
        

def debug(errorCode, pos):
    pass
