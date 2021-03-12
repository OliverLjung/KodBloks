from classes import Game, Window
import getCodes 
import pygame
import time

class Main:

    def __init__(self):
        self._codes = getCodes.getCodes()
        if self._codes == -1:
            # Start or Finish missing
            print("Start or Finish missing")
        else:
            self._game = Game()
            self._window = Window()
            self._game.start()
            self._character = self._game.character
            
            self.start()

    def start(self):
        for code in self._codes:
            self.function(int(code))
            self._game.update()
            if self._game.run == True:
                self._window.draw(self._game)
                time.sleep(0.3)

        self._window.drawScore(self._character)
        time.sleep(2)


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