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

    def start(self):
        self._codes = getCodes.getCodes()
        print(self._codes)
        if self._codes == -1: 
            print("Start or stop code is missing")
            return

        elif self._codes == -2:
            print("Condition code is missing")
            return

        for codeList in self._codes:
            self.function(codeList)
            self._game.update()
            if self._game.run == True:
                self._window.draw(self._game)
                time.sleep(0.3)
            else:
                self._window.draw(self._game)
                break

        self._window.drawScore(self._character)
        time.sleep(2)
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

        elif code == 79:
            # Turn right
            self._character.turnRight()

        elif code == 61:
            # Turn left
            self._character.turnLeft()

        elif code == 47:
            # Start whileloop
            print(f"Cond: {codeList[1]}")
            while self.condition(codeList[1]):
                for codeSubList in codeList[2]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw(self._game)
                        time.sleep(0.3)
                        self.function(codeSubList)
                    else:
                        self._window.draw(self._game)
                        time.sleep(0.3)
                        main()
           elif code == 59:
            # Start if-statement
            print(f"Cond: {codeList[1]}")
            if self.condition(codeList[1]):
                for codeSubList in codeList[2]:
                    self._game.update()
                    if self._game.run == True:
                        self._window.draw(self._game)
                        time.sleep(0.3)
                        self.function(codeSubList)
                    else:
                        self._window.draw(self._game)
                        time.sleep(0.3)
                        main()
           
        
        self._game.update()
        if self._game.run == True:
            self._window.draw(self._game)
            time.sleep(0.3)
        else:
            self._window.draw(self._game)
            time.sleep(0.3)
            main()


    def condition(self, code):
        if code == 109:
            cond = self._character.pathAhead()
        elif code == 121:
            cond = self._character.notFinished()
        print(cond)
        return cond

    @property
    def game(self):
        return self._game

def main():
    run = True
    while run:
        game = Main()
        # Station logic
        ### takes picture when some event is given
        
        havePicture = False
        while not havePicture:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    game.game.run = False
                    raise SystemExit
                elif event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_SPACE:
                        getCodes.getPic()
                        havePicture = True

        time.sleep(1)

        os.system("java -cp topcodes.jar topcodes.DebugWindow > fil")
                        
        game.start()
        if game.game.run is False:
            main()


if __name__ == "__main__":
    pygame.init()
    main()
