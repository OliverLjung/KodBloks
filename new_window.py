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
    text_rect.center = (245, 45)

    exit_text = font.render('Exit', True, red,)
    exit_rect = exit_text.get_rect()
    exit_rect.center = (250, 610)

    #text size
    text_font = pygame.font.Font('freesansbold.ttf', 17)       
    
    start_text = text_font.render('Start block: ', True, black,)
    start_rect = start_text.get_rect()
    start_rect = (45, 62)

    stop_text = text_font.render('Stop block: ', True, black,)
    stop_rect = stop_text.get_rect()
    stop_rect = (45, 106)

    run = False
    while not run:
        bg = pygame.image.load('bg.jpg')
        for event in pygame.event.get():
            windw.blit(bg, (0, 0))
            windw.blit(text, text_rect)
            windw.blit(exit_text, exit_rect)
            
            i = 70 
            while i >= 70 and i <= 580:
                pygame.draw.circle(windw, black, (37,i), 5) #Punkt    
                i+= 45
            
            windw.blit(start_text, start_rect)
            windw.blit(stop_text, stop_rect)

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