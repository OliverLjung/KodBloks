from classes import Game, Window, HelpWindow
import getCodes
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

class Main:
    """
    Class: Handels game-logic and runs the game, a new instance of Main is a new game, new map etc.
    """

    def __init__(self):
        self._game = Game()
        self._window = Window(self._game)
        self._character = self._game.character
        self._window.draw()

        self.ifHasFailed = False

    def reset(self):
        """
        Function: Resets the state of game but the map remains the same.
        """
        self._game.reset()
        self._window = Window(self._game)
        self._character = self._game.character
        self._window.draw()

        self.ifHasFailed = False

    def start(self):
        """
        Function: Gets codes from webcam, starts game and runs until game is finished or character has bumped into a wall.
        """
        self._codes = getCodes.get_codes()

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
        """
        Function: args codeList, from current list of codes (codeList) get the current functionality.
        In this game it is:

        while - 47,
        if - 59,
        else - 103,
        pathAhead - 109,
        pathLeft - 115,
        pathRight - 117,
        notFinished - 121,
        forward - 87,
        turnLeft - 61,
        turnRight - 79
        """
        self._game.update()
        self._window.draw()
        if self._game.run == False:
            return
            
        code = codeList[0]
        if type(code) is list:
            code = code[0]

        if code == 87:
            # Move forward
            self._character.move_forward()
            self.ifHasFailed = False

        elif code == 79:
            # Turn right
            self._character.turn_right()
            self.ifHasFailed = False

        elif code == 61:
            # Turn left
            self._character.turn_left()
            self.ifHasFailed = False

        elif code == 47:
            # Start whileloop
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
        """
        Function: args code, from given code representing a statement, checks if that statement is true or not and returns either True or False.
        In this game it is:

        pathAhead - 109,
        pathLeft - 115,
        pathRight - 117,
        notFinished - 121
        """
        if code == 109:
            cond = self._character.path_ahead()
        elif code == 121:
            cond = self._character.not_finished()
        elif code == 117:
            cond = self._character.path_right()
        elif code == 121:
            cond = self._character.path_left()
        return cond

    @property
    def game(self):
        """
        Function: game getter
        """
        return self._game

    @property
    def character(self):
        """
        Function: character getter
        """
        return self._character

    @property
    def window(self):
        """
        Function: window getter
        """
        return self._window
    

def main(new=0):
    """
    Function: args new=0, handles game and button input to wait or execute.
    if new == 1: reset the game should remain the same.
    """
    global game
    pygame.init()

    if Config.stopThreads == True:
        stop_game()

    if new == 1:
        # map should remain the same
        game.reset()

    else:
        if type(game) == type(None):
            game = Main()
        elif game.game.finished:
            game.window.draw_score()
            game = Main()
        else:
            game.window.draw_score()
            game.reset()
            

    run = True
    
    runPos = (1300, 600)
    helpPos = (1300, 200)

    while run:
        if Config.stopThreads == True:
            stop_game()
        # Station logic
        ### takes picture when some event is given
        game.window.draw()
        havePicture = False
        while not havePicture:
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    game.game.run = False
                    stop_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    xPos, yPos = pygame.mouse.get_pos()
                    if (helpPos[0]<= xPos <= helpPos[0]+215) and (helpPos[1] <= yPos <= helpPos[1]+70):
                        help_window = HelpWindow()
                        help_window.draw_help()
                        main(1)
                    elif (runPos[0]<= xPos <= runPos[0]+180) and (runPos[1] <= yPos <= runPos[1]+70):
                        game.window.draw_compile()
                        # getCodes.get_pic()
                        havePicture = True
                elif event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        stop_game()
                    

        os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
                        
        game.start()
        if game.game.run is False:
            game.window.draw()
            main()
        

def stop_game():
    """
    Function: stops and joins main and camera thread and exits the program.
    """
    global camera
    Config.stopThreads_setter(True)
    cam.join()
    pygame.quit()
    print("EXITED")
    raise SystemExit

if __name__ == "__main__":
    game = None
    try:
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("music/game.ogg")
        pygame.mixer.music.play(loops=-1)
    except Exception:
        print("Couldn't load audio.")
    
    Config.stopThreads_setter(False)
    cam = threading.Thread(target= Camera.camera_thread, args =(lambda : Config.stopThreads, ))
    cam.start()

    main()
    