import pygame
import random

class Game:

    def __init__(self):
        "Initilizes a Game"
        self.start()

    def start(self):
        "Starts a Game"
        self._run = True
        self._map = []
        self._mapSize = (0, 0)
        self.getMap()
        self._character = Character(self)

<<<<<<< Updated upstream
    def updata(self, character):
        "Checks entities status in map"
        for subList in self._map:
            for element in subList:
                if character.pos == element:
                    if element == 1:
                        # Collision
                        self._run = False
                    elif element == "p":
                        # Scores
                        character.score += 1

                    elif element == "f":
=======
    def update(self):
        "Checks entities status in map"
        y = -1
        for subList in self._map:
            x = -1
            y+=1
            for _ in subList:
                x+=1
                if self._character.pos == (x, y):
                    if self._map[y][x] == 1:
                        # Collision
                        self._run = False
                    elif self._map[y][x] == "p":
                        # Scores
                        self._character.score += 1

                    elif self._map[y][x] == "f":
>>>>>>> Stashed changes
                        # Finish
                        self._character.score += 10
                        print(f"Score = {self._character.score}")
                        self.run = False
<<<<<<< Updated upstream
=======
                        break

        self.updateMap()


    def updateMap(self):
        "Updates status for every bit in map"
        y = -1
        for subList in self._map:
            x = -1
            y+=1
            for _ in subList:
                x+=1
                if self._character.pos == (x, y):
                    self._map[y][x] = "c"
                    if self._map[y][x] == "p":
                        self._map[y][x] = 0
                elif self._map[y][x] == "c":
                    self._map[y][x] = 0

>>>>>>> Stashed changes

    def getMap(self):
        "Gets a map for Game to played on"

        randomMapInt = random.randint(1, 1)
        _file = open(f"maps/map{randomMapInt}.txt", "r")
        _lines = _file.readlines()
        _width = 0
        _height = 0
        for line in _lines:
            lineList = []
            for bit in line:
                if bit != " " and bit != "\n":
                    if bit.isnumeric():
                        if bit == "0":
                            rand = random.randint(0,5)
                            if rand==0:
                                lineList.append("p")
                            else:
                                lineList.append(int(bit))
                        else:
                            lineList.append(int(bit))
                    else:
                        lineList.append(bit)

            self._map.append(lineList)

        self._mapSize = (len(self._map[0]), len(self._map))
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

    @property
    def character(self):
        return self._character

    @run.setter
    def run(self, status):
        self._run = status
        

class Character():
    def __init__(self, game):
        self._direction = "EAST"
        self._game = game
        self._score = 0
        self._pos = self.getInitPos()
        print(self._pos)

    def getInitPos(self):
        y = -1
        for sublist in self._game.map:
            x = -1
            y+=1
            for element in sublist:
                x+=1
                if element == "c":
                    return (x,y)

    def moveForward(self):
        "Move character forward one block in its current direction: returns True if the move is valid and False if its not"
        x = self._pos[0]
        y = self._pos[1]

        if self._direction == "EAST":
            x+=1
        elif self._direction == "WEST":
            x-=1
        elif self._direction == "NORTH":
            y-=1
        elif self._direction == "SOUTH":
            y+=1
        
        self._pos = (x,y)

    def turnRight(self):
        if self._direction == "EAST":
<<<<<<< Updated upstream
            self._direction == "SOUTH"
        elif self._direction == "WEST":
            self._direction == "NORTH"
        elif self._direction == "NORTH":
            self._direction == "EAST"
        elif self._direction == "SOUTH":
            self._direction == "WEST"

    def turnLeft(self):
        if self._direction == "EAST":
            self._direction == "NORTH"
        elif self._direction == "WEST":
            self._direction == "SOUTH"
        elif self._direction == "NORTH":
            self._direction == "WEST"
        elif self._direction == "SOUTH":
            self._direction == "EAST"
=======
            self._direction = "SOUTH"

        elif self._direction == "WEST":
            self._direction = "NORTH"

        elif self._direction == "NORTH":
            self._direction = "EAST"

        elif self._direction == "SOUTH":
            self._direction = "WEST"


    def turnLeft(self):
        if self._direction == "EAST":
            self._direction = "NORTH"

        elif self._direction == "WEST":
            self._direction = "SOUTH"

        elif self._direction == "NORTH":
            self._direction = "WEST"
            
        elif self._direction == "SOUTH":
            self._direction = "EAST"

>>>>>>> Stashed changes

    @property    
    def direction(self):
        return self._direction

    @property
    def score(self):
        return self._score

<<<<<<< Updated upstream
=======
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, xy):
        self._pos = xy

>>>>>>> Stashed changes
    @score.setter
    def score(self, points):
        self._score = points


class Window:
    def __init__(self):
        self.win_width = 515
        self.win_height = 515
        self.FPS = 60

        self.window = pygame.display.set_mode((self.win_width, self.win_height)) # Window
        pygame.display.set_caption("Maze Game") # Window title

        #rbg
        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        self.width = 46
        self.height = 46
        self.margin = 5


    def draw(self, game):
    
        self.clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False
            
        self.window.fill(self.black)

        # Draw the grid
        currentMap = game.map
<<<<<<< Updated upstream
        print(game.map)
        print(game.mapSize)
        for x in range(0, game.mapSize[0]):
            for y in range(0 ,game.mapSize[1]):
                print(f"Current koord: ({x}, {y}) \n")
=======
        for sublist in game.map:
            print(sublist)
        print("New frame\n\n")
        for x in range(0, game.mapSize[0]):
            for y in range(0 ,game.mapSize[1]):
>>>>>>> Stashed changes
                if currentMap[y][x] == 1:
                    self.cell_color = self.white
                elif currentMap[y][x] == 0 or currentMap[y][x] == "f":
                    self.cell_color = self.black
                elif currentMap[y][x] == "c":
                    self.cell_color = self.red
                elif currentMap[y][x] == "p":
                    self.cell_color = self.green

                pygame.draw.rect(self.window, self.cell_color,
                                [(self.margin + self.width) * x + self.margin,
                                (self.margin + self.height) * y + self.margin,
                                self.width,
                                self.height]) 
            
        self.clock.tick(self.FPS)
        pygame.display.flip()

