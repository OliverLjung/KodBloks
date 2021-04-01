from classes import Game, Window
import getCodes 
import pygame
import time
import os
import cv2

from pygame.locals import *


class Main:

    def __init__(self):
        self._game = Game()
        self._window = Window(self._game)
        self._character = self._game.character
        self._window.draw(self._game)

        self.n = 0
        self.ifHasFailed = False

    def start(self):
        self._codes = getCodes.getCodes()
        if self._codes == -1: 
            return

        elif self._codes == -2:
            return

        for codeList in self._codes:
            self.function(codeList)
            self._game.update()
            if self._game.run == True:
                self._window.draw(self._game)
            else:
                self._window.draw(self._game)
                break

        main()

    def function(self, codeList):
        self._game.update()
        if self._game.run == False:
            return
            
        code = codeList[0]
        if type(code) is list:
            code = code[0]

        self.n+=1
        print(f"\nFrame {self.n}")
        print(f"List: {codeList}")
        print(f"Code: {code}")

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
            print(f"Cond: {codeList[1]}")
            while self.condition(codeList[1]):
                for codeSubList in codeList[2]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw(self._game)
                        self.function(codeSubList)
                    else:
                        self._window.draw(self._game)
                        main()
            self.ifHasFailed = False

        elif code == 59:
            # Start if-statement
            print(f"Cond: {codeList[1]}")
            if self.condition(codeList[1]):
                self.ifHasFailed = False
                for codeSubList in codeList[2]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw(self._game)
                        self.function(codeSubList)
                    else:
                        self._window.draw(self._game)
                        main()
            else:
                self.ifHasFailed = True

        elif code == 103:
            # Start else-statement
            if self.ifHasFailed:
                for codeSubList in codeList[1]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw(self._game)
                        self.function(codeSubList)
                    else:
                        self._window.draw(self._game)
                        main()
            self.ifHasFailed = False
        
        
        self._game.update()
        if self._game.run == True:
            self._window.draw(self._game)
        else:
            self._window.draw(self._game)
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
        print(cond)
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
    

def main():
    global game
    if type(game) is Main:
        game.window.drawScore(game.character)
    run = True
    while run:
        pygame.init()
        game = Main()
        # Station logic
        ### takes picture when some event is given
        game.window.draw(game.game)
        havePicture = False
        while not havePicture:
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    game.game.run = False
                    raise SystemExit
                elif event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        inp = input("Do you want to exit the program (y/n):")
                        if "y" in inp.lower():
                            raise SystemExit
                        else:
                            main()
                    elif event.key == K_SPACE:
                        # getCodes.getPic()
                        havePicture = True

        os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
                        
        game.start()
        if game.game.run is False:
            main()


if __name__ == "__main__":
    game = None
    main()