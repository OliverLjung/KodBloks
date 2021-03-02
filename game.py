# import pygame
import random

class Game:

    def __init__(self):
        "Initilizes a Game"

        self._map = []

    def start(self):
        "Starts a Game"

        self.getMap()
        self.drawGame()

    def drawGame(self):
        "Draws the current state of the Game"
        for line in self._map:
            print(line)

    def getMap(self):
        "Gets a map for Game to played on"

        randomMapInt = random.randint(1, 1)
        _file = open(f"maps/map{randomMapInt}.txt", "r")
        _lines = _file.readlines()
        for line in _lines:
            lineList = []
            for bit in line:
                if bit.isnumeric():
                    lineList.append(int(bit))
            self._map.append(lineList)

        _file.close()

# TEST
mygame = Game()
mygame.start()