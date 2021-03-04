import pygame
import random

class Game:

    def __init__(self):
        "Initilizes a Game"
        self._character = Character()
        self.start()

    def start(self):
        "Starts a Game"
        self._run = True
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

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, status):
        self._run = status
        

class Character():
    def __init__(self):
        pass


class Window:
    def __init__(self):
        self.win_width = 515
        self.win_height = 515
        self.FPS = 60

        self.window = pygame.display.set_mode((self.win_width, self.win_height)) # Window
        pygame.display.set_caption("Maze Grid") # Window title

        #rbg
        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)

        self.width = 46
        self.height = 46
        self.margin = 5


        self.grid = []
        # Size of the grid
        for row in range(10):
            self.grid.append([])
            for column in range(10):
                self.grid[row].append(0)


    def draw(self, game):
    
        self.clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run(False)
                print("You have quit the window")
            
        self.window.fill(self.black)

        # Draw the grid
        currentMap = game.map
        for row in range(game.mapSize[1]):
            for column in range(game.mapSize[0]):
                if currentMap[row][column] == 1:
                    self.cell_color = self.white
                elif currentMap[row][column] == 0:
                    self.cell_color = self.black
                elif currentMap[row][column] == "h":
                    self.cell_color = self.black
                elif currentMap[row][column] == "p":
                    self.cell_color = self.black
                

                # if self.grid[row][column] == 1:
                #     self.cell_color = self.red
                pygame.draw.rect(self.window, self.cell_color,
                                [(self.margin + self.width) * column + self.margin,
                                (self.margin + self.height) * row + self.margin,
                                self.width,
                                self.height]) 
            
        self.clock.tick(self.FPS)
        pygame.display.flip()

