import pygame
import random
from pygame.locals import *

from var import Config

class Game:

    def __init__(self):
        """
        Function: Starts a Game
        """
        self._run = True
        self._collision = False
        self._finished = False

        self._map = []
        self._map_size = (0, 0)
        self.get_map()
        self._startingMap = self.copy_map()
        self.start()

    def start(self):
        """
        Function: Starts a Game
        """
        self._run = True
        self._collision = False
        self._finished = False
        self._character = Character(self)

    def copy_map(self):
        """
        Function: Copying the map
        """
        copy = []
        for line in self._map:
            copy.append(line.copy())
        return copy

    def reset(self):
        """
        Function: Reset the game
        """
        self._map = self._startingMap
        self.start()

    def update(self):
        """
        Function: Checks entities status in map
        """
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

        self.update_map()


    def update_map(self):
        """
        Function: Updates status for every bit in map
        """
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


    def get_map(self):
        """
        Function: Gets a map for Game to played on
        """

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

        self._map_size = (len(self._map[0]), len(self._map))
        _file.close()

    @property
    def map(self):
        return self._map

    @property
    def map_size(self):
        return self._map_size

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
    """
    Class: Functionally of the character
    """
    def __init__(self, game):
        self._direction = "EAST"
        self._game = game
        self._score = 0
        self._pos = self.get_init_pos()

    def get_init_pos(self):
        """
        Function: Get the position in the map.
        """
        y = -1
        for sublist in self._game.map:
            x = -1
            y+=1
            for element in sublist:
                x+=1
                if element == "c":
                    return (x,y)

    def move_forward(self):
        """Function: Move character forward one block in its current direction: 
        returns True if the move is valid and False if its not
        """
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

    def turn_right(self):
        """
        Function: The turn right block, the character will turn right
        """
        if self._direction == "EAST":
            self._direction = "SOUTH"

        elif self._direction == "WEST":
            self._direction = "NORTH"

        elif self._direction == "NORTH":
            self._direction = "EAST"

        elif self._direction == "SOUTH":
            self._direction = "WEST"


    def turn_left(self):
        """
        Function: The turn left block, the character will turn left
        """
        if self._direction == "EAST":
            self._direction = "NORTH"

        elif self._direction == "WEST":
            self._direction = "SOUTH"

        elif self._direction == "NORTH":
            self._direction = "WEST"
            
        elif self._direction == "SOUTH":
            self._direction = "EAST"

    def path_ahead(self):
        """
        Function: The path ahead block, the character can move forward
        """
    
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

    def path_right(self):
        """
        Function: The path right block, the character can turn right
        """
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

    def path_left(self):
        """
        Function: The path left block, the character can turn left
        """
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

        
    def not_finished(self):
        """
        Function: The not finished block, if the game is not finished yet
        """
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
    """
    Class: Draws the window for the game.
    """
    def __init__(self, game):
        self._winWidth = 1920
        self._windHeight = 1080
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
        self.width = int(self._winWidth/game.map_size[0] - self.margin)
        self.height = int(self._windHeight/game.map_size[1] - self.margin)
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
        """
        Function: Draws the grid, help button and the run button.
        """

        # detta måste garantera att
        game = self._game
        self.clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False
                Config.stopThreads_setter(True)
            
        self.window.fill(self.black)

        # Draw the grid
        currentMap = game.map
        for x in range(0, game.map_size[0]):
            for y in range(0 ,game.map_size[1]):
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
        _helpPos = (1300, 200)
        font = pygame.font.Font('freesansbold.ttf', 80)
        self._helpText = font.render('HELP', True, self.red,)
        self._helpReact = self._helpText.get_rect()
        self._helpReact = _helpPos
        self.window.blit(self._helpText, self._helpReact)
        
        #Run knappen
        runPos = (1300, 600)
        self._runText = font.render("RUN", True, self.green)
        self._runReact = self._runText.get_rect()
        self._runReact = runPos
        self.window.blit(self._runText, self._runReact)
            
        self.clock.tick(self.FPS)
        pygame.display.flip()

    def draw_compile(self):
        """
        Function: Draws 'compling, please wait' when the user click the run button.
        """
        font = pygame.font.Font('freesansbold.ttf', 100)
        compText = font.render("Compling, please wait.", True, self.red)
        compRect = compText.get_rect()
        compRect.center = (self._winWidth//2 , self._windHeight//2 - 40)
        self.window.blit(compText, compRect)
        pygame.display.flip()


    def draw_score(self):
        """
        Function: Draws the score and if you press 'New game' then a new map is going to show up.
        """
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
                        Config.stopThreads_setter(True)

class HelpWindow:
    """
    Class: This class is for the help window when you press the help button.
    """
    def __init__(self):
        pygame.font.init()

        self.bg = pygame.image.load('graphics\helpbg.jpg') #Bakgrund 

        # self._windw = pygame.display.set_mode([self.bg.get_width(), self.bg.get_height()])
        # self._windw = pygame.display.set_mode(((1920-self.bg.get_width())//2 , ((1080-self.bg.get_height())//2), pygame.FULLSCREEN)
        self._windw = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Instruction window")
        
        self.black = (0, 0, 0)
        self.white = (255, 255,255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

    def sve(self):
        """
        Function: Draws the swedish text on the help window.
        """

        self._textFont = pygame.font.Font('freesansbold.ttf', 14)
        self._startText = self._textFont.render('Spelet startas, början av sekvensen.', True, self.white,)
        self._startRect = self._startText.get_rect()
        self._startRect.center = (260, 70)
        self._stopText = self._textFont.render('Spelet avslutas, slutet av sekvensen.', True, self.white,)
        self._stopRect = self._stopText.get_rect()
        self._stopRect.center = (260, 115)
        self._stopRect.center = (260, 115)
        self.turnR_text = self._textFont.render('Karaktären svänger höger.', True, self.white,)
        self._turnRect = self.turnR_text.get_rect()
        self._turnRect.center = (260, 160)
        self._turnLText = self._textFont.render('Karaktären svänger vänster.', True, self.white,)
        self._turnLRect = self._turnLText.get_rect()
        self._turnLRect.center = (255, 205)
        self._goForwardText = self._textFont.render('Karaktären kommer att gå framåt.', True, self.white,)
        self._goForwardRect = self._goForwardText.get_rect()
        self._goForwardRect.center = (295, 250)
        self._whileText = self._textFont.render('Flödesuttalande, kod körs upprepade gånger.', True, self.white,)
        self._whileRect = self._whileText.get_rect()
        self._whileRect.center = (295, 296)
        self._ifText = self._textFont.render('Koden körs när if-satsen är sant.', True, self.white,)
        self._ifRect = self._ifText.get_rect()
        self._ifRect.center = (213, 340)
        self._elseText = self._textFont.render('Koden körs när if-satsen är falsk.', True, self.white,)
        self._elseRect = self._elseText.get_rect()
        self._elseRect.center = (240, 385)
        self._pathAheadText = self._textFont.render('Möjligheten att gå framåt.', True, self.white,)
        self._pathAheadRect = self._pathAheadText.get_rect()
        self._pathAheadRect.center = (267, 431)
        self._pathRightText = self._textFont.render('Möjligheten att svänga höger.', True, self.white,)
        self._pathRightRect = self._pathRightText.get_rect()
        self._pathRightRect.center = (271, 476)
        self._pathLeftText = self._textFont.render('Möjligheten att svänga vänster.', True, self.white,)
        self._pathLeftRect = self._pathLeftText.get_rect()
        self._pathLeftRect.center = (268, 521)
        self.not_finished_text = self._textFont.render("Karaktären har inte nått målet", True, self.white,)
        self._notFinishedRect = self.not_finished_text.get_rect()
        self._notFinishedRect.center = (298, 566)

        self._windw.blit(self._startText, self._startRect)
        self._windw.blit(self._stopText, self._stopRect)
        self._windw.blit(self.turnR_text, self._turnRect)
        self._windw.blit(self._turnLText, self._turnLRect)
        self._windw.blit(self._goForwardText, self._goForwardRect)
        self._windw.blit(self._whileText, self._whileRect)
        self._windw.blit(self._ifText, self._ifRect)
        self._windw.blit(self._elseText, self._elseRect)
        self._windw.blit(self._elseText, self._elseRect)
        self._windw.blit(self._pathAheadText, self._pathAheadRect)
        self._windw.blit(self._pathRightText, self._pathRightRect)
        self._windw.blit(self._pathLeftText, self._pathLeftRect)
        self._windw.blit(self.not_finished_text, self._notFinishedRect)


    def eng(self):
        """
        Function: Draws the english text on the help window.
        """
        self._textFont = pygame.font.Font('freesansbold.ttf', 14)
        self._startText = self._textFont.render('The game starts, beginning of the sequence.', True, self.white,)
        self._startRect = self._startText.get_rect()
        self._startRect.center = (289, 71)
        self._stopText = self._textFont.render('Game ends, end of the sequence.', True, self.white,)
        self._stopRect = self._startText.get_rect()
        self._stopRect.center = (285, 115)
        self.turnR_text = self._textFont.render('The character turns right.', True, self.white,)
        self._turnRect = self.turnR_text.get_rect()
        self._turnRect.center = (260, 161)
        self._turnLText = self._textFont.render('The character turns left.', True, self.white,)
        self._turnLRect = self._turnLText.get_rect()
        self._turnLRect.center = (240, 205)
        self._goForwardText = self._textFont.render('The character will move forward.', True, self.white,)
        self._goForwardRect = self._goForwardText.get_rect()
        self._goForwardRect.center = (295, 250)
        self._whileText = self._textFont.render('Flow statement, code executes repeatedly.', True, self.white,)
        self._whileRect = self._whileText.get_rect()
        self._whileRect.center = (285, 295)
        self._ifText = self._textFont.render('Runs the code when the if statement is true.', True, self.white,)
        self._ifRect = self._ifText.get_rect()
        self._ifRect.center = (255, 340)
        self._elseText = self._textFont.render('Runs the code when the if statement is false.', True, self.white,)
        self._elseRect = self._elseText.get_rect()
        self._elseRect.center = (280, 385)       
        self._pathAheadText = self._textFont.render('The opportunity to move forward.', True, self.white,)
        self._pathAheadRect = self._pathAheadText.get_rect()
        self._pathAheadRect.center = (294, 430)
        self._pathRightText = self._textFont.render('The opportunity to turn right.', True, self.white,)
        self._pathRightRect = self._pathRightText.get_rect()
        self._pathRightRect.center = (271, 475)
        self._pathLeftText = self._textFont.render('The opportunity to turn left.', True, self.white,)
        self._pathLeftRect = self._pathLeftText.get_rect()
        self._pathLeftRect.center = (255, 520) 
        self.not_finished_text = self._textFont.render("Character has not reached to goal.", True, self.white,)
        self._notFinishedRect = self.not_finished_text.get_rect()
        self._notFinishedRect.center = (325, 566)
        
        self._windw.blit(self._startText, self._startRect)
        self._windw.blit(self._stopText, self._stopRect)      
        self._windw.blit(self.turnR_text, self._turnRect)   
        self._windw.blit(self._turnLText, self._turnLRect)   
        self._windw.blit(self._goForwardText, self._goForwardRect)
        self._windw.blit(self._whileText, self._whileRect)
        self._windw.blit(self._ifText, self._ifRect)
        self._windw.blit(self._elseText, self._elseRect)
        self._windw.blit(self._pathAheadText, self._pathAheadRect)
        self._windw.blit(self._pathAheadText, self._pathAheadRect)
        self._windw.blit(self._pathRightText, self._pathRightRect)
        self._windw.blit(self._pathLeftText, self._pathLeftRect)
        self._windw.blit(self.not_finished_text, self._notFinishedRect)  

    def draw_help(self):
        """
        Function: Draws the actuall text on the window and draws the button that changes the language and the exit button.
        """
        help_window = HelpWindow()

        #text size
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self._textFont = pygame.font.Font('freesansbold.ttf', 17)  
        self._langFont = pygame.font.Font('freesansbold.ttf', 17)
        #Title
        self.text = self.font.render('Instruktioner-Instructions', True, self.black,)
        self._textRect = self.text.get_rect()
        self._textRect.center = (230, 45)

        #Exit rektangeln
        self._exitText = self.font.render('Exit', True, self.red,)
        self._exitReact = self._exitText.get_rect()
        self._exitReact.center = (250, 610)

        #Välj språk, Sve eller Eng
        self._pickLangText = self._langFont.render('Sve/Eng', True, self.white,)
        self._pickLangRect = self._pickLangText.get_rect()
        self._pickLangRect = (405, 38)

        #Start block
        self._startText = self._textFont.render('Start block: ', True, self.black,)
        self._startRect = self._startText.get_rect()
        self._startRect = (29, 61)

        #Stop block
        self._stopText = self._textFont.render('Stop block: ', True, self.black,)
        self._stopRect = self._stopText.get_rect()
        self._stopRect = (29, 106)

        #Turn right block
        self._rightText = self._textFont.render('Turn right block: ', True, self.black)
        self._rightRect = self._rightText.get_rect()
        self._rightRect = (29, 151)

        #Turn left block
        self._leftText = self._textFont.render('Turn left block: ', True, self.black)
        self._leftRect = self._leftText.get_rect()
        self._leftRect = (29, 195)

        #Go forward block
        self._forwardText = self._textFont.render('Go forward block: ', True, self.black)
        self._forwardRect = self._forwardText.get_rect()
        self._forwardRect = (29, 241)

        #While block
        self._whileText = self._textFont.render('While block: ', True, self.black)
        self._whileRect = self._whileText.get_rect()
        self._whileRect = (29, 286)

        #If-block
        self._ifText = self._textFont.render('If block: ', True, self.black)
        self._ifRect = self._ifText.get_rect()
        self._ifRect = (29, 331)

        #Else block
        self._elseText = self._textFont.render('Else block: ', True, self.black)
        self._elseRect = self._elseText.get_rect()
        self._elseRect = (29, 376)

        #Path ahead block
        self._aheadText = self._textFont.render('Path ahead block: ', True, self.black)
        self._aheadRect= self._aheadText.get_rect()
        self._aheadRect = (29, 421)

        #Path right block
        self._pathRightText = self._textFont.render('Path right block: ', True, self.black)
        self._pathRightRect= self._pathRightText.get_rect()
        self._pathRightRect = (29, 466)

        #Path left block
        self._pathLeftText = self._textFont.render('Path left block: ', True, self.black)
        self._pathLeftRect= self._pathLeftText.get_rect()
        self._pathLeftRect = (29, 511)

        #Not finished block
        self._notFinText = self._textFont.render('Not finished block: ', True, self.black)
        self._notFinRect = self._notFinText.get_rect()
        self._notFinRect = (29, 556)
        

        self._windw.blit(self.bg, (0, 0))
        self._windw.blit(self.text, self._textRect)
        self._windw.blit(self.bg, (0, 0))
        self._windw.blit(self.text, self._textRect)
        self._windw.blit(self.exit_text, self._exitReact)
        self._windw.blit(self._pickLangText, self._pickLangRect)
        self._windw.blit(self._startText, self._startRect)
        self._windw.blit(self._stopText, self._stopRect)
        self._windw.blit(self._rightText, self._rightRect)
        self._windw.blit(self._leftText, self._leftRect)
        self._windw.blit(self._forwardText, self._forwardRect)
        self._windw.blit(self._whileText, self._whileRect)
        self._windw.blit(self._ifText, self._ifRect)
        self._windw.blit(self._elseText, self._elseRect)
        self._windw.blit(self._aheadText, self._aheadRect)
        self._windw.blit(self._pathRightText, self._pathRightRect)
        self._windw.blit(self._pathLeftText, self._pathLeftRect)
        self._windw.blit(self._notFinText, self._notFinRect)
        
        help_window.sve()
        pygame.display.flip()

        lang = "sve"
        hasChanged = False
        run = True
        while run:
            if hasChanged:
                self._windw.blit(self.bg, (0, 0))
                self._windw.blit(self.text, self._textRect)
                self._windw.blit(self.bg, (0, 0))
                self._windw.blit(self.text, self._textRect)
                self._windw.blit(self.exit_text, self._exitReact)
                self._windw.blit(self._pickLangText, self._pickLangRect)
                self._windw.blit(self._startText, self._startRect)
                self._windw.blit(self._stopText, self._stopRect)
                self._windw.blit(self._rightText, self._rightRect)
                self._windw.blit(self._leftText, self._leftRect)
                self._windw.blit(self._forwardText, self._forwardRect)
                self._windw.blit(self._whileText, self._whileRect)
                self._windw.blit(self._ifText, self._ifRect)
                self._windw.blit(self._elseText, self._elseRect)
                self._windw.blit(self._aheadText, self._aheadRect)
                self._windw.blit(self._pathRightText, self._pathRightRect)
                self._windw.blit(self._pathLeftText, self._pathLeftRect)
                self._windw.blit(self._notFinText, self._notFinRect)
                if lang == "sve":
                    help_window.sve()
                elif lang == "eng":
                    help_window.eng()
                pygame.display.flip()
                hasChanged = False

            for event in pygame.event.get():          
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self._mx, self._my = pygame.mouse.get_pos()
                    #Exit knappen
                    if self._mx >= 225 and self._mx <= 275 and self._my >= 600 and self._my <= 620:
                        run = False
                        break
                    #Sve knappen
                    if self._mx >= 405 and self._mx <= 430 and self._my >= 38 and self._my <= 51:
                        lang = "sve"
                        hasChanged = True
                    #Eng knappen
                    if self._mx >= 440 and self._mx <= 469 and self._my >= 40  and self._my <= 55:
                        lang = "eng"
                        hasChanged = True
                if event.type == pygame.QUIT: 
                    run =  False
                    break

                if event.type == KEYDOWN or event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        exitPressed=True
                        Config.stopThreads_setter(True)
                        run =  False
                        break