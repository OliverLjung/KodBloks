import pygame
import random
from pygame.locals import *

from var import Config

class Game:

    def __init__(self):
        "Initilizes a Game"
        self._run = True
        self._collision = False
        self._finished = False

        self._map = []
        self._mapSize = (0, 0)
        self.getMap()
        self._startingMap = self.copyMap()
        self.start()

    def start(self):
        "Starts a Game"
        self._run = True
        self._collision = False
        self._finished = False
        self._character = Character(self)

    def copyMap(self):
        copy = []
        for line in self._map:
            copy.append(line.copy())
        return copy

    def reset(self):
        self._map = self._startingMap
        self.start()

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
                        self._collision = True
                        self._run = False
                    elif self._map[y][x] == "p":
                        # Scores
                        self._character.score += 1

                    elif self._map[y][x] == "f":
                        # Finish
                        self._finished = True
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

    @property
    def collision(self):
        return self._collision

    @property
    def finished(self):
        return self._finished

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

        if (x>=0) and (y>=0):
            self._pos = (x,y)
        else:
            print("index out of bounds")

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
        
        if self._game.map[y][x] == "f":
            return False
        elif self._game.finished:
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
        self.win_width = 1920
        self.win_height = 1080
        self.FPS = 60

        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Window
        pygame.display.set_caption("Maze Game") # Window title

        #rbg
        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        # säkerställer att alla bloken får plats
        self.margin = 5
        self.width = int(self.win_width/game.mapSize[0] - self.margin)
        self.height = int(self.win_height/game.mapSize[1] - self.margin)
        if self.height < self.width:
            self.width = self.height
        
        self._game = game


        self._wallImage = pygame.image.load("graphics/wall.jpg")
        self._wallImage = pygame.transform.scale(self._wallImage, (self.width, self.width))

        self._pathImage = pygame.image.load("graphics/path.jpg")
        self._pathImage = pygame.transform.scale(self._pathImage, (self.width, self.width))

        self._finishImage = pygame.image.load("graphics/finish.jpg")
        self._finishImage = pygame.transform.scale(self._finishImage, (self.width, self.width))

        self._characterImage = pygame.image.load(f"graphics/character{game.character.direction.lower()}.jpg")
        self._characterImage = pygame.transform.scale(self._characterImage, (self.width, self.width))

        self._foodImage = pygame.image.load("graphics/food.jpg")
        self._foodImage = pygame.transform.scale(self._foodImage, (self.width, self.width))

    def draw(self):
        # detta måste garantera att
        game = self._game
        self.clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False
                Config.stopThreadsSetter(True)
            
        self.window.fill(self.black)

        # Draw the grid
        currentMap = game.map
        for x in range(0, game.mapSize[0]):
            for y in range(0 ,game.mapSize[1]):
                # if currentMap[y][x] == 1:
                #     self.cell_color = self.white
                # elif currentMap[y][x] == 0 or currentMap[y][x] == "f":
                #     self.cell_color = self.black
                # elif currentMap[y][x] == "c":
                #     self.cell_color = self.red
                # elif currentMap[y][x] == "p":
                #     self.cell_color = self.green

                # pygame.draw.rect(self.window, self.cell_color,
                #                 [(self.margin + self.width) * x + self.margin,
                #                 (self.margin + self.height) * y + self.margin,
                #                 self.width,
                #                 self.height]) 

                if currentMap[y][x] == 1:
                    currentEntityImage = self._wallImage
                elif currentMap[y][x] == 0:
                    currentEntityImage = self._pathImage
                elif currentMap[y][x] == "f":
                    currentEntityImage = self._finishImage
                elif currentMap[y][x] == "c":
                    currentEntityImage = pygame.image.load(f"graphics/character{game.character.direction.lower()}.jpg")
                elif currentMap[y][x] == "p":
                    currentEntityImage = self._foodImage

                self.window.blit(currentEntityImage, [(self.margin + self.width) * x + self.margin,
                                (self.margin + self.width) * y + self.margin])

                    
        #Hjälp knappen
        helpPos = (1300, 200)
        font = pygame.font.Font('freesansbold.ttf', 80)
        self.help_text = font.render('HELP', True, self.red,)
        self.help_react = self.help_text.get_rect()
        self.help_react = helpPos
        self.window.blit(self.help_text, self.help_react)
        
        #Run knappen
        runPos = (1300, 600)
        self.run_text = font.render("RUN", True, self.green)
        self.run_react = self.run_text.get_rect()
        self.run_react = runPos
        self.window.blit(self.run_text, self.run_react)
            
        self.clock.tick(self.FPS)
        pygame.display.flip()

    def drawCompile(self):
        font = pygame.font.Font('freesansbold.ttf', 100)
        compText = font.render("Compling, please wait.", True, self.red)
        compRect = compText.get_rect()
        compRect.center = (self.win_width//2 , self.win_height//2 - 40)
        self.window.blit(compText, compRect)
        pygame.display.flip()


    def drawScore(self):
        character = self._game.character
        pygame.font.init()
        textFont = pygame.font.SysFont("arial", 100)
        text = textFont.render(f"Score: {character.score}", True, (255,0,0), (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1920//2, 1080//2)

        exitFont = pygame.font.SysFont("arial", 64)
        exitText = exitFont.render("New Game", True, (255,0,0), (0,0,0))
        exitTextRect = exitText.get_rect()
        exitPos = (1920//2, 1080-50)
        exitTextRect.center = exitPos

        self.window.blit(text, textRect)
        self.window.blit(exitText, exitTextRect)
        
        exitPressed = False
        while not exitPressed:
            pygame.display.flip()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    exitPressed=True
                if event.type == MOUSEBUTTONDOWN:
                    mPos = pygame.mouse.get_pos()
                    if (exitPos[0]-150<=mPos[0]<=exitPos[0]+150) and (exitPos[1]-30<=mPos[1]<=exitPos[1]+30):
                        exitPressed=True
                if event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        exitPressed=True
                        Config.stopThreadsSetter(True)

class HelpWindow:
    def __init__(self):
        pygame.font.init()

        self.bg = pygame.image.load('graphics\helpbg.jpg') #Bakgrund 

        # self.windw2 = pygame.display.set_mode([self.bg.get_width(), self.bg.get_height()])
        # self.windw2 = pygame.display.set_mode(((1920-self.bg.get_width())//2 , ((1080-self.bg.get_height())//2), pygame.FULLSCREEN)
        self.windw2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Instruction window")
        
        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

    def sve(self):
        self.text_font = pygame.font.Font('freesansbold.ttf', 14)
        self.start_text = self.text_font.render('Spelet startas, början av sekvensen.', True, self.white,)
        self.start_rect = self.start_text.get_rect()
        self.start_rect.center = (260, 70)
        self.stop_text = self.text_font.render('Spelet avslutas, slutet av sekvensen.', True, self.white,)
        self.stop_rect = self.stop_text.get_rect()
        self.stop_rect.center = (260, 115)
        self.stop_rect.center = (260, 115)
        self.turnR_text = self.text_font.render('Karaktären svänger höger.', True, self.white,)
        self.turnR_rect = self.turnR_text.get_rect()
        self.turnR_rect.center = (260, 160)
        self.turnL_text = self.text_font.render('Karaktären svänger vänster.', True, self.white,)
        self.turnL_rect = self.turnL_text.get_rect()
        self.turnL_rect.center = (255, 205)
        self.go_forward_text = self.text_font.render('Karaktären kommer att gå framåt.', True, self.white,)
        self.go_forward_rect = self.go_forward_text.get_rect()
        self.go_forward_rect.center = (295, 250)
        self.while_text_b = self.text_font.render('Flödesuttalande, kod körs upprepade gånger.', True, self.white,)
        self.while_rect_b = self.while_text_b.get_rect()
        self.while_rect_b.center = (295, 296)
        self.if_text_b = self.text_font.render('Koden körs när if-satsen är sant.', True, self.white,)
        self.if_rect_b = self.if_text_b.get_rect()
        self.if_rect_b.center = (213, 340)
        self.else_text_b = self.text_font.render('Koden körs när if-satsen är falsk.', True, self.white,)
        self.else_rect_b = self.else_text_b.get_rect()
        self.else_rect_b.center = (240, 385)
        self.path_ahead_text = self.text_font.render('Möjligheten att gå framåt.', True, self.white,)
        self.path_ahead_rect = self.path_ahead_text.get_rect()
        self.path_ahead_rect.center = (267, 431)
        self.path_right_text = self.text_font.render('Möjligheten att svänga höger.', True, self.white,)
        self.path_right_rect = self.path_right_text.get_rect()
        self.path_right_rect.center = (271, 476)
        self.path_left_text = self.text_font.render('Möjligheten att svänga vänster.', True, self.white,)
        self.path_left_rect = self.path_left_text.get_rect()
        self.path_left_rect.center = (268, 521)
        self.not_finished_text = self.text_font.render("Karaktären har inte nått målet", True, self.white,)
        self.not_finished_rect = self.not_finished_text.get_rect()
        self.not_finished_rect.center = (298, 566)

        self.windw2.blit(self.start_text, self.start_rect)
        self.windw2.blit(self.stop_text, self.stop_rect)
        self.windw2.blit(self.turnR_text, self.turnR_rect)
        self.windw2.blit(self.turnL_text, self.turnL_rect)
        self.windw2.blit(self.go_forward_text, self.go_forward_rect)
        self.windw2.blit(self.while_text_b, self.while_rect_b)
        self.windw2.blit(self.if_text_b, self.if_rect_b)
        self.windw2.blit(self.else_text_b, self.else_rect_b)
        self.windw2.blit(self.else_text_b, self.else_rect_b)
        self.windw2.blit(self.path_ahead_text, self.path_ahead_rect)
        self.windw2.blit(self.path_right_text, self.path_right_rect)
        self.windw2.blit(self.path_left_text, self.path_left_rect)
        self.windw2.blit(self.not_finished_text, self.not_finished_rect)


    def eng(self):
        self.text_font = pygame.font.Font('freesansbold.ttf', 14)
        self.start_text = self.text_font.render('The game starts, beginning of the sequence.', True, self.white,)
        self.start_rect = self.start_text.get_rect()
        self.start_rect.center = (289, 71)
        self.stop_text = self.text_font.render('Game ends, end of the sequence.', True, self.white,)
        self.stop_rect = self.start_text.get_rect()
        self.stop_rect.center = (285, 115)
        self.turnR_text = self.text_font.render('The character turns right.', True, self.white,)
        self.turnR_rect = self.turnR_text.get_rect()
        self.turnR_rect.center = (260, 161)
        self.turnL_text = self.text_font.render('The character turns left.', True, self.white,)
        self.turnL_rect = self.turnL_text.get_rect()
        self.turnL_rect.center = (240, 205)
        self.go_forward_text = self.text_font.render('The character will move forward.', True, self.white,)
        self.go_forward_rect = self.go_forward_text.get_rect()
        self.go_forward_rect.center = (295, 250)
        self.while_text_b = self.text_font.render('Flow statement, code executes repeatedly.', True, self.white,)
        self.while_rect_b = self.while_text_b.get_rect()
        self.while_rect_b.center = (285, 295)
        self.if_text_b = self.text_font.render('Runs the code when the if statement is true.', True, self.white,)
        self.if_rect_b = self.if_text_b.get_rect()
        self.if_rect_b.center = (255, 340)
        self.else_text_b = self.text_font.render('Runs the code when the if statement is false.', True, self.white,)
        self.else_rect_b = self.else_text_b.get_rect()
        self.else_rect_b.center = (280, 385)       
        self.path_ahead_text = self.text_font.render('The opportunity to move forward.', True, self.white,)
        self.path_ahead_rect = self.path_ahead_text.get_rect()
        self.path_ahead_rect.center = (294, 430)
        self.path_right_text = self.text_font.render('The opportunity to turn right.', True, self.white,)
        self.path_right_rect = self.path_right_text.get_rect()
        self.path_right_rect.center = (271, 475)
        self.path_left_text = self.text_font.render('The opportunity to turn left.', True, self.white,)
        self.path_left_rect = self.path_left_text.get_rect()
        self.path_left_rect.center = (255, 520) 
        self.not_finished_text = self.text_font.render("Character has not reached to goal.", True, self.white,)
        self.not_finished_rect = self.not_finished_text.get_rect()
        self.not_finished_rect.center = (325, 566)
        
        self.windw2.blit(self.start_text, self.start_rect)
        self.windw2.blit(self.stop_text, self.stop_rect)      
        self.windw2.blit(self.turnR_text, self.turnR_rect)   
        self.windw2.blit(self.turnL_text, self.turnL_rect)   
        self.windw2.blit(self.go_forward_text, self.go_forward_rect)
        self.windw2.blit(self.while_text_b, self.while_rect_b)
        self.windw2.blit(self.if_text_b, self.if_rect_b)
        self.windw2.blit(self.else_text_b, self.else_rect_b)
        self.windw2.blit(self.path_ahead_text, self.path_ahead_rect)
        self.windw2.blit(self.path_ahead_text, self.path_ahead_rect)
        self.windw2.blit(self.path_right_text, self.path_right_rect)
        self.windw2.blit(self.path_left_text, self.path_left_rect)
        self.windw2.blit(self.not_finished_text, self.not_finished_rect)  

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
        run = True
        while run:
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
                        break
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
                    break

                if event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        exitPressed=True
                        Config.stopThreadsSetter(True)
                        run =  False
                        break