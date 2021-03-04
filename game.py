from classes import Game, Window
import getCodes 
import pygame
import time

class Main:

    def __init__(self):
        self._codes = getCodes.getCodes()
        self._mygame = Game()
        self._myWindow = Window()
        self._mygame.start()
        self._character = self._mygame.character
        
        self.start()

    def start(self):
        for code in self._codes:
            self.function(code)
            if self._mygame.run == True:
                self._myWindow.draw(self._mygame)
                time.sleep(0.3)


    def function(self, code):
        if code == 87:
            self._character.moveForward()

        elif code == 79:
            self._character.turnRight()

        elif code == 61:
            self._character.turnLeft()


if __name__ == "__main__":
    pygame.init()
    game = Main()