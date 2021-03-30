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
                        # Finish
                        self.run = False
                        self._character.score += 10

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
                    if self._map[y][x] == "f":
                        self._map[y][x] = "f"
                    else:
                        self._map[y][x] = "c"
                elif self._map[y][x] == "c":
                    self._map[y][x] = 0


    def getMap(self):
        "Gets a map for Game to played on"

        randomMapInt = random.randint(1, 3)
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

    def pathAhead(self):
        x = self._pos[0]
        y = self._pos[1]

        if self._game.map[y][x] == "f":
            return False

        if self._direction == "EAST":
            x+=1
        elif self._direction == "WEST":
            x-=1
        elif self._direction == "NORTH":
            y-=1
        elif self._direction == "SOUTH":
            y+=1
        
        if self._game.map[y][x] == 1:
            return False
        else:
            return True

    def pathRight(self):
        x = self._pos[0]
        y = self._pos[1]
        if self._game.map[y][x] == "f":
            return False
        if self._direction == "EAST":
            y+=1
        elif self._direction == "WEST":
            y-=1
        elif self._direction == "NORTH":
            x+=1
        elif self._direction == "SOUTH":
            x-=1

        if self._game.map[y][x] == 1:
            return False
        else:
            return True

    def pathLeft(self):
        x = self._pos[0]
        y = self._pos[1]
        if self._game.map[y][x] == "f":
            return False
        if self._direction == "EAST":
            y+=1
        elif self._direction == "WEST":
            y+-1
        elif self._direction == "NORTH":
            x+=1
        elif self._direction == "SOUTH":
            x=-1

        if self._game.map[y][x] == 1:
            return False
        else:
            return True

        
    def notFinished(self):
        x = self._pos[0]
        y = self._pos[1]
        
        if self._game.map[x][y] == "f":
            return False
        else:
            return True



    @property    
    def direction(self):
        return self._direction

    @property
    def score(self):
        return self._score

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, xy):
        self._pos = xy

    @score.setter
    def score(self, points):
        self._score = points


class Window:
    black = (0, 0, 0)
    white = (255, 255,255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    def __init__(self, game):
        self.win_width = 800
        self.win_height = 600
        self.FPS = 60

        self.window = pygame.display.set_mode((self.win_width, self.win_height)) # Window
        pygame.display.set_caption("Maze Game") # Window title

        #rbg
        

        # säkerställer att alla bloken får plats
        self.margin = 5
        # self.width = self.win_width/game.mapSize[0] - self.margin
        # self.height = self.win_height/game.mapSize[1] - self.margin

        # Så help och run knappen får plats
        self.width = 55 - self.margin 
        self.height = 55 - self.margin
        

    def drawHelp(self):
        self.win_width2 = 470
        self.win_height2 = 600
        self.windw2 = pygame.display.set_mode((self.win_width2, self.win_height2))
        pygame.display.set_caption("Instruction window")

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.text = self.font.render('Instruktioner-Instructions', True, Window.black,)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (250, 50)

        #Exit rektangeln
        self.exit_text = self.font.render('Exit', True, Window.red,)
        self.exit_react = self.exit_text.get_rect()
        self.exit_react.center = (250, 600)
        
        self.run = False
        while not self.run:
            self.bg = pygame.image.load('bg.jpg') #Bakgrund 
            self.windw2.blit(self.bg, (0, 0))
            pygame.display.flip()

            self.windw2.blit(self.text, self.text_rect)
            pygame.display.flip()
            
            for event in pygame.event.get():
                self.windw2.blit(self.bg, (0, 0))
                self.windw2.blit(self.text, self.text_rect)
                self.windw2.blit(self.exit_text, self.exit_react)
                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN: #Exit knappen
                    self.mx, self.my = pygame.mouse.get_pos()
                    if self.mx >= 225 and self.mx <= 275 and self.my >= 600 and self.my <= 620:
                        run = False
                        raise SystemExit

                if event.type == pygame.QUIT: 
                    run =  False
                    raise SystemExit

    
        

    def draw(self, game):
        # detta måste garantera att
    
        self.clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False
                raise SystemExit
            
        self.window.fill(self.black)

        # Draw the grid
        currentMap = game.map
        for x in range(0, game.mapSize[0]):
            for y in range(0 ,game.mapSize[1]):

                #Hjälp knappen
                font = pygame.font.Font('freesansbold.ttf', 40)
                self.help_text = font.render('HELP', True, self.red,)
                self.help_react = self.help_text.get_rect()
                self.help_react = (630, 60)

                self.window.blit(self.help_text, self.help_react)
                pygame.display.flip()


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


    def drawScore(self, character):
        print(f"Score = {character.score}")
