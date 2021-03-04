from classes import Game, Window
import getCodes 
import pygame
import time

class Main:

    def __init__(self):
        self._codes = getCodes.getCodes()
<<<<<<< Updated upstream
        self._mygame = Game()
        self._myWindow = Window()
        self._mygame.start()
        self._character = self._mygame.character
=======
        self._game = Game()
        self._window = Window()
        self._game.start()
        self._character = self._game.character
>>>>>>> Stashed changes
        
        self.start()

    def start(self):
        for code in self._codes:
<<<<<<< Updated upstream
            self.function(code)
            if self._mygame.run == True:
                self._myWindow.draw(self._mygame)
                time.sleep(0.3)
=======
            self.function(int(code))
            self._game.update()
            if self._game.run == True:
                self._window.draw(self._game)
                time.sleep(0.3)
                
>>>>>>> Stashed changes


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