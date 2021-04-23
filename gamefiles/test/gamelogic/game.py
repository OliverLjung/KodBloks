from classes import Game, Window, HelpWindow
import pygame
import time
import os

from pygame.locals import *

# for getting codes
import re
import os.path
import math
# for getting picture
import numpy
import cv2
import threading
## alt
import pygame.camera
import pygame.mixer

from var import Config
from camera import Camera

expectedResult = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
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

nr = 0


class Main:

    def __init__(self):
        self._game = Game()
        self._window = Window(self._game)
        self._character = self._game.character
        self._window.draw()

        self.n = 0
        self.ifHasFailed = False

    def reset(self):
        self._game.reset()
        self._window = Window(self._game)
        self._character = self._game.character
        self._window.draw()

        self.n = 0
        self.ifHasFailed = False

    def start(self):
        global expectedResult
        global nr
        nr += 1
        if nr == 21:
            stopGame()

        self._codes = expectedResult[f"{nr}"]
        print(f"Initial codes: {self._codes}\n")
        if self._codes == -1: 
            # missing start or stop
            self._window.draw()
            return

        elif self._codes == -2:
            # missing condition
            self._window.draw()
            return

        for codeList in self._codes:
            self.function(codeList)
            self._game.update()
            if self._game.run == True:
                self._window.draw()
            else:
                self._window.draw()
                break

        main()

    def function(self, codeList):
        self._game.update()
        self._window.draw()
        if self._game.run == False:
            return
            
        code = codeList[0]
        if type(code) is list:
            code = code[0]

        self.n+=1
        # print(f"\nFrame {self.n}")
        # print(f"List: {codeList}")
        # print(f"Code: {code}")

        if code == 87:
            # Move forward
            self._character.moveForward()
            self.ifHasFailed = False

        elif code == 79:
            # Turn right
            self._character.turnRight()
            self.ifHasFailed = False

        elif code == 61:
            # Turn left
            self._character.turnLeft()
            self.ifHasFailed = False

        elif code == 47:
            # Start whileloop
            # print(f"Cond: {codeList[1]}")
            while self.condition(codeList[1]):
                for codeSubList in codeList[2]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw()
                        self.function(codeSubList)
                    else:
                        self._window.draw()
                        main()
            self.ifHasFailed = False

        elif code == 59:
            # Start if-statement
            # print(f"Cond: {codeList[1]}")
            if self.condition(codeList[1]):
                self.ifHasFailed = False
                for codeSubList in codeList[2]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw()
                        self.function(codeSubList)
                    else:
                        self._window.draw()
                        main()
            else:
                self.ifHasFailed = True

        elif code == 103:
            # Start else-statement
            if self.ifHasFailed:
                for codeSubList in codeList[1]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw()
                        self.function(codeSubList)
                    else:
                        self._window.draw()
                        main()
            self.ifHasFailed = False
        
        
        self._game.update()
        if self._game.run == True:
            self._window.draw()
        else:
            self._window.draw()
            main()


    def condition(self, code):
        if code == 109:
            cond = self._character.pathAhead()
        elif code == 121:
            cond = self._character.notFinished()
        elif code == 117:
            cond = self._character.pathRight()
        elif code == 121:
            cond = self._character.pathLeft()
        # print(cond)
        return cond

    @property
    def game(self):
        return self._game

    @property
    def character(self):
        return self._character

    @property
    def window(self):
        return self._window
    

def main(new=0):
    global game
    pygame.init()

    if Config.stopThreads is True:
        stopGame()

    if new == 1:
        # map should remain the same
        print("RESET")
        game.reset()

    else:
        if type(game) == type(None):
            print("INIT")
            game = Main()
        elif game.game.finished:
            print("FINISH!!!")
            game.window.drawScore()
            game = Main()
        else:
            print("FAILED")
            game.window.drawScore()
            game.game.reset()
            

    run = True
    
    runPos = (1300, 600)
    helpPos = (1300, 200)

    while run:
        # Station logic
        ### takes picture when some event is given
        game.window.draw()
        havePicture = False
        while not havePicture:
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    game.game.run = False
                    stopGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = pygame.mouse.get_pos()
                    if (helpPos[0]<= x_pos <= helpPos[0]+215) and (helpPos[1] <= y_pos <= helpPos[1]+70):
                        help_window = HelpWindow()
                        help_window.drawHelp()
                        main(1)
                    elif (runPos[0]<= x_pos <= runPos[0]+180) and (runPos[1] <= y_pos <= runPos[1]+70):
                        game.window.drawCompile()
                        havePicture = True
                elif event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        stopGame()

                        
        game.start()
        if game.game.run is False:
            game.window.draw()
            main()
        

def stopGame():
    global camera
    Config.stopThreadsSetter(True)
    cam.join()
    pygame.quit()
    print("EXITED")
    raise SystemExit

if __name__ == "__main__":
    game = None
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("music/game.ogg")
    pygame.mixer.music.play(loops=-1)
    
    Config.stopThreadsSetter(False)
    cam = threading.Thread(target= Camera.cameraThread, args =(lambda : Config.stopThreads, ))
    cam.start()

    main()
    