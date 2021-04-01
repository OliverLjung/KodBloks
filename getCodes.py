# imports

# for getting codes
import re
import os.path
import time
import math
# for getting picture
import cv2
## alt
import pygame
import pygame.camera
from pygame.locals import *
pygame.init()
pygame.camera.init()


def getPic():
    # try:
    #     camera = cv2.VideoCapture(cv2.CAP_DSHOW)
    #     time.sleep(0.5)  # If you don't wait, the image will be dark
    #     check, image = camera.read()
    #     if check:
    #         cv2.imwrite("bild.jpg", image)
    #     else:
    #         raise(Exception)
    #     camera.release() 
    # except Exception:
    #     print("Error in camera")
    
    camlist = pygame.camera.list_cameras()
    if camlist:
        cam = pygame.camera.Camera(camlist[0],(1280 , 720))
        cam.start()
        time.sleep(0.5)
        image = cam.get_image()
        pygame.image.save(image, "bild.jpg")

    else:
        print("Error in camera")
    
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
        debug("noline")
        return -1

    lib.remove(stoplib)
    lib.append(stoplib)

    xDiff = (stopPos[0]- startPos[0])
    yDiff = (stopPos[1] - startPos[1])
    dirVector = (xDiff, yDiff)
    dirVectorLength = math.sqrt(dirVector[0]**2 + dirVector[1]**2)

    if dirVectorLength == 0:
        # Didnt find start and stop
        debug("noline")
        return -1

    dirVector = (dirVector[0]/dirVectorLength , dirVector[1]/dirVectorLength)

    if dirVector == (0,0):
        # Didnt find start and stop
        debug("noline")
        return -1

    n = 5
    linePos = startPos
    searchForCond = False
    condVector = (-dirVector[1], dirVector[0])
    finished = False
    codeArea = [startPos,startPos]

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
                        postemp = pos
                        linePosCond = pos
                    else:
                        codes.append((code, pos))
                        lib.remove(sublib)

        if searchForCond:
            linePosCond = ((linePosCond[0]+n*condVector[0]), (linePosCond[1]+n*condVector[1]))
            codeArea = [(linePosCond[0]-50, linePosCond[1]-50) , (linePosCond[0]+50, linePosCond[1]+50)]
            if (linePosCond[0] > stopPos[0]+500*condVector[0]) and (linePosCond[1] > stopPos[1]+500*condVector[0]):
                debug("nocondition", postemp)
                return -2
        else:
            linePos = ((linePos[0]+n*dirVector[0]), (linePos[1]+n*dirVector[1]))
            codeArea = [(linePos[0]-50, linePos[1]-50) , (linePos[0]+50, linePos[1]+50)]
            if (linePos[0] > stopPos[0]) and (linePos[1] > stopPos[1]):
                finished = True
                    
    if codes == []:
        debug("noline")
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
            debug("condition", pos)
            raise SystemExit
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
            debug("condition", pos)
            raise SystemExit
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

    
        

def debug(errorCode, pos=(0,0)):
    if errorCode.lower() == "noline":
        message = "Start or Finish is missing"
    elif errorCode.lower() == "nocondition":
        message = "Condition is missing"
    elif errorCode.lower() == "nostop":
        message = "Stop for while/is/else is missing"

    debug = DebugWindow()
    debug.drawErrorPic(message, pos)

class DebugWindow():
    def __init__(self, mode=False):
        self.isControlled = mode
        self.picture = pygame.image.load("bild.jpg")
        pygame.init()
        self.pictureWidth = self.picture.get_width()
        self.pictureHeight = self.picture.get_height()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Debug Window")
        if self.isControlled:
            #tänkte kanske en kontrollerad debugger där man kan välja att hoppa stegvis för att följa exekvering
            pass

    def drawErrorPic(self, message, pos=(0,0)):
        "Draws arrow and message to given position"

        self.window.fill((255,255,255))
        self.window.blit(self.picture, (0, 0))

        pygame.font.init()

        textFont = pygame.font.SysFont("arial", 32)
        text = textFont.render(message, True, (0, 0, 0), (255,255,255))
        textRect = text.get_rect()

        exitFont = pygame.font.SysFont("arial", 64)
        exitText = exitFont.render("EXIT", True, (255,0,0), (255,255,255))
        exitTextRect = exitText.get_rect()
        exitPos = (1920//2, 1080-50)
        exitTextRect.center = exitPos

        if pos == (0,0):
            textRect.center = (self.pictureWidth//2, self.pictureHeight//2)
        elif pos[1] > 1920//2:
            arrowPoint = (pos[0], pos[1]+30)
            arrow = (
                arrowPoint,
                (arrowPoint[0]-60, arrowPoint[1]+30),
                (arrowPoint[0]-30, arrowPoint[1]+30),
                (arrowPoint[0]-30, arrowPoint[1]+90),
                (arrowPoint[0]+30, arrowPoint[1]+90),
                (arrowPoint[0]+30, arrowPoint[1]+30),
                (arrowPoint[0]+60, arrowPoint[1]+30)
                )
            pygame.draw.polygon(self.window, (255, 0 , 0), arrow)
            textRect.center = (pos[0], pos[1]+30+90+10)
        elif pos[1] < 1920//2:
            arrowPoint = (pos[0], pos[1]-30)
            arrow = (
                arrowPoint,
                (arrowPoint[0]-60, arrowPoint[1]-30),
                (arrowPoint[0]-30, arrowPoint[1]-30),
                (arrowPoint[0]-30, arrowPoint[1]-90),
                (arrowPoint[0]+30, arrowPoint[1]-90),
                (arrowPoint[0]+30, arrowPoint[1]-30),
                (arrowPoint[0]+60, arrowPoint[1]-30)
                )
            pygame.draw.polygon(self.window, (255, 0 , 0), arrow)
            textRect.center = (pos[0], pos[1]-30-90-10)

        self.window.blit(text, textRect)
        self.window.blit(exitText, exitTextRect)
        
        run=True
        while run:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run=False
                if event.type == MOUSEBUTTONDOWN:
                    mPos = pygame.mouse.get_pos()
                    if (exitPos[0]-16<=mPos[0]<=exitPos[0]+16) and (exitPos[1]-16<=mPos[1]<=exitPos[1]+16):
                        run=False
            pygame.display.update() 
        pygame.quit()
    def draw(self, pos):
        pass
