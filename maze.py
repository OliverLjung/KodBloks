import pygame
#import random


win_width = 515
win_height = 515
FPS = 60

window = pygame.display.set_mode((win_width, win_height)) # Window
pygame.display.set_caption("Maze Grid") # Window title

#rbg
black = (0, 0, 0)
white = (255, 255,255)
red = (255, 0, 0)

width = 46
height = 46
margin = 5

# Size ofg the grid
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("You have quit the window")
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                column = position[0] // (width + margin)
                row = position[1] // (width + margin)

                grid[row][column] = 1

                print("Clicked", position, "grid coordinates: ", row, column)

        window.fill(black)

        # Draw the grid
        for row in range(10):
            for column in range(10):
                cell_color = white
                if grid[row][column] == 1:
                    cell_color = red
                pygame.draw.rect(window, cell_color,
                                [(margin + width) * column + margin,
                                (margin + height) * row + margin,
                                width,
                                height]) 
        
        clock.tick(FPS)
        pygame.display.flip()



main()
pygame.quit()