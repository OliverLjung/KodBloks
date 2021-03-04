# import pygame
import random

class Game:

    def __init__(self):
        "Initilizes a Game"
        self._character = Character()
        self.start()

    def start(self):
        "Starts a Game"
        self._map = []
        self._mapSize = (0, 0)
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
        _width = 0
        _height = 0
        for line in _lines:
            _height +=1
            lineList = []
            for bit in line:
                if bit.isnumeric():
                    _width +=1
                    lineList.append(int(bit))
            self._map.append(lineList)

        self._mapSize = (_width, _height)
        _file.close()

    @property
    def map(self):
        return self._map

    @property
    def mapSize(self):
        return self._mapSize


class Character():
    def __init__(self):
        pass


# TEST
mygame = Game()
mygame.start()