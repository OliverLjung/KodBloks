import pygame
import os


white = (255, 255,255)
red = (255, 0, 0)
black = (0,0,0)

win_width = 500
win_height = 650
windw = pygame.display.set_mode((win_width, win_height))

def sve():
    sve_text_font = pygame.font.Font('freesansbold.ttf', 13)
    sve_text = sve_text_font.render('Spelet startas', True, black,)
    sve_rect = sve_text.get_rect()
    sve_rect.center = (200, 65)

    windw.blit(sve_text, sve_rect)




def eng():
    eng_text_font = pygame.font.Font('freesansbold.ttf', 14)
    start_text = eng_text_font.render('The game is started.', True, red,)
    start_rect = start_text.get_rect()
    start_rect.center = (213, 73)
    
    stop_text = eng_text_font.render('The game is ended.', True, red,)
    stop_rect = start_text.get_rect()
    stop_rect.center = (210, 117)


    windw.blit(start_text, start_rect)
    windw.blit(stop_text, stop_rect)


def main():

    pygame.init()

    # windw = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Instruction window")


    #text size
    text_font = pygame.font.Font('freesansbold.ttf', 17)  
    lang_font = pygame.font.Font('freesansbold.ttf', 17)
    font = pygame.font.Font('freesansbold.ttf', 25)

    text = font.render('Instruktioner-Instructions', True, black,)
    text_rect = text.get_rect()
    text_rect.center = (230, 45)

    exit_text = font.render('Exit', True, red,)
    exit_rect = exit_text.get_rect()
    exit_rect.center = (250, 610)

    #Välj språk, Sve eller Eng
    pick_lang_text = lang_font.render('Sve/Eng', True, red,)
    pick_lang_rect = pick_lang_text.get_rect()
    pick_lang_rect = (405, 38)

    
    
    start_text = text_font.render('Start block: ', True, black,)
    start_rect = start_text.get_rect()
    start_rect = (45, 63)

    stop_text = text_font.render('Stop block: ', True, black,)
    stop_rect = stop_text.get_rect()
    stop_rect = (45, 107)


    #Draws initial image before changes can be applied
    bg = pygame.image.load('bg.jpg')
        
    windw.blit(bg, (0, 0))
    windw.blit(text, text_rect)
    windw.blit(exit_text, exit_rect)
    windw.blit(pick_lang_text, pick_lang_rect)
    
    i = 70 
    while i >= 70 and i <= 580:
        pygame.draw.circle(windw, black, (37,i), 5) #Punkt    
        i+= 45
    
    windw.blit(start_text, start_rect)
    windw.blit(stop_text, stop_rect)

    change = False
    run = False
    while not run:
        if change:
            bg = pygame.image.load('bg.jpg')
            
            windw.blit(bg, (0, 0))
            windw.blit(text, text_rect)
            windw.blit(exit_text, exit_rect)
            windw.blit(pick_lang_text, pick_lang_rect)
            
            i = 70 
            while i >= 70 and i <= 580:
                pygame.draw.circle(windw, black, (37,i), 5) #Punkt    
                i+= 45
            
            windw.blit(start_text, start_rect)
            windw.blit(stop_text, stop_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    print(mx, my)
                    if mx >= 225 and mx <= 275 and my >= 600 and my <= 620:
                        run = False
                        raise SystemExit
                    if mx >= 405 and mx <= 430 and my >= 38 and my <= 51:
                        sve()
                    if mx >= 440 and mx <= 469 and my >= 40  and my <= 55:
                        eng()

            pygame.display.flip()     


            if event.type == pygame.QUIT: 
                run =  False
                raise SystemExit
main()

pygame.quit()