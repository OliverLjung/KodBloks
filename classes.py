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
        
    
    def __init__(self, game):
        self.win_width = 800
        self.win_height = 600
        self.FPS = 60

        self.window = pygame.display.set_mode((self.win_width, self.win_height)) # Window
        pygame.display.set_caption("Maze Game") # Window title

        #rbg

        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        

        # säkerställer att alla bloken får plats
        self.margin = 5
        # self.width = self.win_width/game.mapSize[0] - self.margin
        # self.height = self.win_height/game.mapSize[1] - self.margin

        # Så help och run knappen får plats
        self.width = 55 - self.margin 
        self.height = 55 - self.margin

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
                
                #Run knappen
                self.run_text = font.render("RUN", True, self.green)
                self.run_react = self.run_text.get_rect()
                self.run_react = (630, 400)
                self.window.blit(self.run_text, self.run_react)
                
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


class HelpWindow:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.bg = pygame.image.load('bg.jpg') #Bakgrund 

        self.windw2 = pygame.display.set_mode([self.bg.get_width(), self.bg.get_height()])
        pygame.display.set_caption("Instruction window")
        
        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

    def sve(self):
        self.sve_text_font = pygame.font.Font('freesansbold.ttf', 14)
        self.start_text = self.sve_text_font.render('Spelet startas, början av sekvensen.', True, self.white,)
        self.start_rect = self.start_text.get_rect()
        self.start_rect.center = (260, 70)
        self.stop_text = self.sve_text_font.render('Spelet avslutas, slutet av sekvensen.', True, self.white,)
        self.stop_rect = self.stop_text.get_rect()
        self.stop_rect.center = (260, 115)

        self.windw2.blit(self.start_text, self.start_rect)
        self.windw2.blit(self.stop_text, self.stop_rect)



    def eng(self):
        self.eng_text_font = pygame.font.Font('freesansbold.ttf', 14)
        self.start_text = self.eng_text_font.render('The game starts, beginning of the sequence.', True, self.white,)
        self.start_rect = self.start_text.get_rect()
        self.start_rect.center = (289, 71)
        self.stop_text = self.eng_text_font.render('Game ends, end of the sequence.', True, self.white,)
        self.stop_rect = self.start_text.get_rect()
        self.stop_rect.center = (285, 115)
        
        self.windw2.blit(self.start_text, self.start_rect)
        self.windw2.blit(self.stop_text, self.stop_rect)        

    def drawHelp(self):

        help_window = HelpWindow()

        #text size
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.text_font = pygame.font.Font('freesansbold.ttf', 17)  
        self.lang_font = pygame.font.Font('freesansbold.ttf', 17)
        #Title
        self.text = self.font.render('Instruktioner-Instructions', True, self.black,)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (230, 45)

        #Exit rektangeln
        self.exit_text = self.font.render('Exit', True, self.red,)
        self.exit_react = self.exit_text.get_rect()
        self.exit_react.center = (250, 610)

        #Välj språk, Sve eller Eng
        self.pick_lang_text = self.lang_font.render('Sve/Eng', True, self.white,)
        self.pick_lang_rect = self.pick_lang_text.get_rect()
        self.pick_lang_rect = (405, 38)

        #Start block
        self.start_text = self.text_font.render('Start block: ', True, self.black,)
        self.start_rect = self.start_text.get_rect()
        self.start_rect = (29, 61)

        #Stop block
        self.stop_text = self.text_font.render('Stop block: ', True, self.black,)
        self.stop_rect = self.stop_text.get_rect()
        self.stop_rect = (29, 106)

        #Turn right block
        self.right_text = self.text_font.render('Turn right block: ', True, self.black)
        self.right_rect = self.right_text.get_rect()
        self.right_rect = (29, 151)

        #Turn left block
        self.left_text = self.text_font.render('Turn left block: ', True, self.black)
        self.left_rect = self.left_text.get_rect()
        self.left_rect = (29, 195)

        #Go forward block
        self.forward_text = self.text_font.render('Go forward block: ', True, self.black)
        self.forward_rect = self.forward_text.get_rect()
        self.forward_rect = (29, 241)

        #While block
        self.while_text = self.text_font.render('While block: ', True, self.black)
        self.while_rect = self.while_text.get_rect()
        self.while_rect = (29, 286)

        #If-block
        self.if_text = self.text_font.render('If block: ', True, self.black)
        self.if_rect = self.if_text.get_rect()
        self.if_rect = (29, 331)

        #Else block
        self.else_text = self.text_font.render('Else block: ', True, self.black)
        self.else_rect = self.else_text.get_rect()
        self.else_rect = (29, 376)

        #Path ahead block
        self.ahead_text = self.text_font.render('Path ahead block: ', True, self.black)
        self.ahead_rect= self.ahead_text.get_rect()
        self.ahead_rect = (29, 421)

        #Path right block
        self.path_right_text = self.text_font.render('Path right block: ', True, self.black)
        self.path_right_rect= self.path_right_text.get_rect()
        self.path_right_rect = (29, 466)

        #Path left block
        self.path_left_text = self.text_font.render('Path left block: ', True, self.black)
        self.path_left_rect= self.path_left_text.get_rect()
        self.path_left_rect = (29, 511)

        #Not finished block
        self.not_fin_text = self.text_font.render('Not finished block: ', True, self.black)
        self.not_fin_rect = self.not_fin_text.get_rect()
        self.not_fin_rect = (29, 556)
        

        self.windw2.blit(self.bg, (0, 0))
        self.windw2.blit(self.text, self.text_rect)
        self.windw2.blit(self.bg, (0, 0))
        self.windw2.blit(self.text, self.text_rect)
        self.windw2.blit(self.exit_text, self.exit_react)
        self.windw2.blit(self.pick_lang_text, self.pick_lang_rect)
        self.windw2.blit(self.start_text, self.start_rect)
        self.windw2.blit(self.stop_text, self.stop_rect)
        self.windw2.blit(self.right_text, self.right_rect)
        self.windw2.blit(self.left_text, self.left_rect)
        self.windw2.blit(self.forward_text, self.forward_rect)
        self.windw2.blit(self.while_text, self.while_rect)
        self.windw2.blit(self.if_text, self.if_rect)
        self.windw2.blit(self.else_text, self.else_rect)
        self.windw2.blit(self.ahead_text, self.ahead_rect)
        self.windw2.blit(self.path_right_text, self.path_right_rect)
        self.windw2.blit(self.path_left_text, self.path_left_rect)
        self.windw2.blit(self.not_fin_text, self.not_fin_rect)
        
        help_window.sve()
        pygame.display.flip()

        lang = "sve"
        hasChanged = False
        run = False
        while not run:
            if hasChanged:
                self.windw2.blit(self.bg, (0, 0))
                self.windw2.blit(self.text, self.text_rect)
                self.windw2.blit(self.bg, (0, 0))
                self.windw2.blit(self.text, self.text_rect)
                self.windw2.blit(self.exit_text, self.exit_react)
                self.windw2.blit(self.pick_lang_text, self.pick_lang_rect)
                self.windw2.blit(self.start_text, self.start_rect)
                self.windw2.blit(self.stop_text, self.stop_rect)
                self.windw2.blit(self.right_text, self.right_rect)
                self.windw2.blit(self.left_text, self.left_rect)
                self.windw2.blit(self.forward_text, self.forward_rect)
                self.windw2.blit(self.while_text, self.while_rect)
                self.windw2.blit(self.if_text, self.if_rect)
                self.windw2.blit(self.else_text, self.else_rect)
                self.windw2.blit(self.ahead_text, self.ahead_rect)
                self.windw2.blit(self.path_right_text, self.path_right_rect)
                self.windw2.blit(self.path_left_text, self.path_left_rect)
                self.windw2.blit(self.not_fin_text, self.not_fin_rect)
                if lang == "sve":
                    help_window.sve()
                elif lang == "eng":
                    help_window.eng()
                pygame.display.flip()
                hasChanged = False

            for event in pygame.event.get():          
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.mx, self.my = pygame.mouse.get_pos()
                    #Exit knappen
                    if self.mx >= 225 and self.mx <= 275 and self.my >= 600 and self.my <= 620:
                        run = False
                        pygame.quit()
                    #Sve knappen
                    if self.mx >= 405 and self.mx <= 430 and self.my >= 38 and self.my <= 51:
                        lang = "sve"
                        hasChanged = True
                    #Eng knappen
                    if self.mx >= 440 and self.mx <= 469 and self.my >= 40  and self.my <= 55:
                        lang = "eng"
                        hasChanged = True
                if event.type == pygame.QUIT: 
                    run =  False
                    pygame.quit()


mywindow = HelpWindow()
mywindow.drawHelp()