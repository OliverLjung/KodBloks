import pygame
import os

def main():

    pygame.init()

    win_width = 500
    win_height = 650
    windw = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Instruction window")

    white = (255, 255,255)
    red = (255, 0, 0)
    black = (0,0,0)


    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render('Instruktioner-Instructions', True, black,)
    text_rect = text.get_rect()
    text_rect.center = (250, 50)

    exit_text = font.render('Exit', True, red,)
    exit_react = exit_text.get_rect()
    exit_react.center = (250, 610)


    run = False
    while not run:
        bg = pygame.image.load('bg.jpg')
        for event in pygame.event.get():
            windw.blit(bg, (0, 0))
            windw.blit(text, text_rect)
            windw.blit(exit_text, exit_react)
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if mx >= 225 and mx <= 275:
                        run = False
                        raise SystemExit
                    if my >= 600 and my <= 620:
                        run = False
                        raise SystemExit

            if event.type == pygame.QUIT: 
                run =  False
                raise SystemExit
main()

pygame.quit()