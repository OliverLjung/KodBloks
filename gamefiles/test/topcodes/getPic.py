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
        codesList.append(codesLib["code"])

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

    while Camera.picReady == False:
        time.sleep(0.1)
    Camera.haltSetter(True)
    while Camera.picReady == False:
        time.sleep(0.1)
    image = cv2.imread("bildSRC.jpg")
    cv2.imwrite("bild.jpg", image)
    Camera.haltSetter(False) 
    getPicFlip()
        

def stopGame():
    global camera
    Config.stopThreadsSetter(True)
    cam.join()
    print("EXITED")
    raise SystemExit

if __name__ == "__main__":    
    Config.stopThreadsSetter(False)
    cam = threading.Thread(target= Camera.cameraThread, args =(lambda : Config.stopThreads, ))
    cam.start()
    time.sleep(3)
    getPic()
    stopGame()

