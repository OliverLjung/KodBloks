import pygame
#import random

class Maze:
    def window(self):
        self.win_width = 515
        self.win_height = 515
        self.FPS = 60

        self.window_s = pygame.display.set_mode((self.win_width, self.win_height)) # Window
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


    def draw(self):
        self.clock = pygame.time.Clock()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.position = pygame.mouse.get_pos()
            self.column = self.position [0] // (self.width + self.margin)
            self.row = self.position [1] // (self.width + self.margin)

            self.grid[self.row][self.column] = 1

            print("Clicked", self.position, "grid coordinates: ", self.row, self.column)

        self.window_s.fill(self.black) # Setting black background

        # Draw the grid
        for row in range(10):
            for column in range(10):
                self.cell_color = self.white
                if self.grid[row][column] == 1:
                    self.cell_color = self.red
                pygame.draw.rect(self.window_s, self.cell_color,
                                [(self.margin + self.width) * column + self.margin,
                                (self.margin + self.height) * row + self.margin,
                                self.width,
                                self.height]) #Drawing the cells 
        
        self.clock.tick(self.FPS)
        pygame.display.flip()




game = Maze()

game.window()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            print("You have quit the window")
    game.draw()



pygame.quit()
