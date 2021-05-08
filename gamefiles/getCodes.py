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

t0 = 0

def buttons_image():
    """
    *NOT IN USE*
    change: buttonPos = [(minX, minY), (maxX, maxY)] to disired area of buttons and add to mainloop in game.py main().

    Function: gets picture from webcam and looks for buttons(bloks) in image and returns str of that button or None if it didnt find.
    In this version:

    "help",
    "run",
    None
    """
    
    buttonPos = [(minX, minY), (maxX, maxY)]
    helpbuttonPos = [(0,0), (0,0)]
    helpButtonCode = 0
    runbuttonPos = [(0,0), (0,0)]
    runButtonCode = 0

    get_pic()
    os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")

    codesLib = get_codes_for_image()
    for lib in codesLib:
        if lib["code"] == helpButtonCode:
            if (helpbuttonPos[0][0] <= lib["pos"][0] <= helpbuttonPos[1][0]) and (helpbuttonPos[0][1] <= lib["pos"][1] <= helpbuttonPos[1][1]):
                return "help"

        elif lib["code"] == runButtonCode:
            if (runbuttonPos[0][0] <= lib["pos"][0] <= runbuttonPos[1][0]) and (runbuttonPos[0][1] <= lib["pos"][1] <= runbuttonPos[1][1]):
                return "run"

    
    get_pic_flip()
    os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
    
    codesLib = get_codes_for_image()
    for lib in codesLib:
        if lib["code"] == helpButtonCode:
            if (helpbuttonPos[0][0] <= lib["pos"][0] <= helpbuttonPos[1][0]) and (helpbuttonPos[0][1] <= lib["pos"][1] <= helpbuttonPos[1][1]):
                return "help"

        elif lib["code"] == runButtonCode:
            if (runbuttonPos[0][0] <= lib["pos"][0] <= runbuttonPos[1][0]) and (runbuttonPos[0][1] <= lib["pos"][1] <= runbuttonPos[1][1]):
                return "run"

    return None
            

def get_codes_for_image():
    """
    Function: Gets codes in "bild.jpg" from "fil" and returns a lib of codes and their position.
    """

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

def get_pic_flip():
    """
    Function: Flips "bild.jpg" and saves the flipped picture in "bild.jpg".
    """
    image = pygame.image.load("bild.jpg")
    image = pygame.transform.flip(image, True, True)
    image = pygame.transform.scale(image, (1920, 1080))
    pygame.image.save(image, "bild.jpg")

def get_pic():
    """
    Function: Halts camera thread and when picture is ready takes the picuture "bildSRC.jpg" and saves the picture in "bild.jpg".
    """
    global triedFlip
    triedFlip = False

    Camera.halt_setter(True)
    while Camera.picReady is False:
        time.sleep(0.1)
    image = cv2.imread("bildSRC.jpg")
    success = False
    while not success:
        success = cv2.imwrite("bild.jpg", image)
    Camera.halt_setter(False) 
        
def get_codes():
    """
    Function: Gets codes in "bild.jpg" from "fil" and sends a list of codes to getSeq() and in the end returns a list of sublists of runnable sequences.
    """
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

    codes = get_seq(codesList)
    return codes

def get_seq(lib):
    """
    Function: args dict; "pos" and "code"
    Creates a runable sequence for dictionary
    returns list
    """
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

    runButtonCode = 0
    helpButtonCode = 0

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

    global t0
    t0 = time.time()

    while not finished:
        if 10 < (time.time() - t0):
            print("Stuck in loop")
            game.stopGame()

        for sublib in lib:
            code = sublib["code"]
            pos = sublib["pos"]
            if (code == runButtonCode) or (code == helpButtonCode):
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
            if (linePosCond[0] > postemp[0]+500*condVector[0]) and (linePosCond[1] > postemp[1]+500*condVector[1]):
                debug("nocondition", postemp)
                return -2
        else:
            linePos = ((linePos[0]+n*dirVector[0]), (linePos[1]+n*dirVector[1]))
            codeArea = [(linePos[0]-50, linePos[1]-50) , (linePos[0]+50, linePos[1]+50)]
            if startPos[0] > stopPos[0]:
                if startPos[1] > stopPos[1]:
                    if (linePos[0] < stopPos[0]) and (linePos[1] < stopPos[1]):
                        finished = True
                else:
                    if (linePos[0] < stopPos[0]) and (linePos[1] > stopPos[1]):
                        finished = True
            else:
                if startPos[1] > stopPos[1]:
                    if (linePos[0] > stopPos[0]) and (linePos[1] < stopPos[1]):
                        finished = True
                else:
                    if (linePos[0] > stopPos[0]) and (linePos[1] > stopPos[1]):
                        finished = True
                             
    if codes == []:
        return -1

    codes.reverse()

    array = get_list_seq(codes, [])

    return array


def get_list_seq(codes, array):
    """
    Function: args array, array;
    Orders codes in first array and adds them to second array.
    If repeated recursivly it creates a runable sequence.
    returns list
    """
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
            game.stopGame()
        else:
            thisList.append(code)
            thisList.append(get_list_seq(codes, thisList))
            return [thisList] + get_list_seq(codes, thisList)
    elif code == ifStartCode:
        thisList.append(code)
        info = codes.pop()
        code = info[0]
        pos = info[1]
        if code not in conditions:
            debug("condition", pos)
            game.stopGame()
        else:
            thisList.append(code)
            thisList.append(get_list_seq(codes, thisList))
            return [thisList] + get_list_seq(codes, thisList)
    elif code == elseStartCode:
        thisList.append(code)
        thisList.append(get_list_seq(codes, thisList))
        return [thisList] + get_list_seq(codes, [])
    else:
        return [[code]] + get_list_seq(codes, [])

    
        

def debug(errorCode, pos=(0,0)):
    """
    Function: args; errorCode, pos (default=(0,0))
    Marks out in picture where and what went wrong
    """
    global triedFlip

    if not triedFlip:
        triedFlip = True
        get_pic_flip()
        os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
        get_codes()

    if errorCode.lower() == "noline":
        message = "Start or Finish is missing"
    elif errorCode.lower() == "nocondition":
        message = "Condition is missing"
    elif errorCode.lower() == "nostop":
        message = "Stop for while/is/else is missing"

    debug = DebugWindow()
    debug.draw_error_pic(message, pos)

class DebugWindow():
    """
    Class:
    Marks out in picture where and what went wrong.
    """
    def __init__(self):
        """
        Function: init DebugWindow class
        """
        self.picture = pygame.image.load("bild.jpg")
        pygame.init()
        self.pictureWidth = self.picture.get_width()
        self.pictureHeight = self.picture.get_height()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Debug Window")

    def draw_error_pic(self, message, pos=(0,0)):
        """
        Function: args; message, pos (default=(0,0)) Draws arrow and message to given position
        """

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
        pygame.display.flip()

        while run:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run=False
                    break
                if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONDOWN:
                    mPos = pygame.mouse.get_pos()
                    if (exitTextRect.topleft[0]<=mPos[0]<=exitTextRect.bottomright[0]) and (exitTextRect.topleft[1]<=mPos[1]<=exitTextRect.bottomright[1]):
                        run=False
                        break
                if event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        Config.stopThreads_setter(True)
                        run = False
                        break
                    