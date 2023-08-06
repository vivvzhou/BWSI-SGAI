from gameplay.ui import UI
from game_menu_ui.button_ui import Button
import os
import pygame

class GameMenu:
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        #  Base window setup
        pygame.init()
        
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 800
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Beaverworks SGAI 2023 - Dead or Alive")
        
        #define fonts
        font = pygame.font.SysFont("arialblack", 40)
        
        #define colors
        TEXT_COL = (255, 255, 255)
        
        #load images
        self.start_img = pygame.image.load('game_menu_ui/images/start_button.png').convert_alpha()
        self.player_guide_img = pygame.image.load('game_menu_ui/images/player_guide_button.png').convert_alpha()
        self.start_hover = pygame.image.load('game_menu_ui/images/start_hover.jpg').convert_alpha()
        self.player_guide_hover = pygame.image.load('game_menu_ui/images/player_guide_hover.jpg').convert_alpha()
        
        #create button instances
        self.start_button = Button(SCREEN_WIDTH, SCREEN_HEIGHT, self.start_img, self.screen, 0.75, self.start_hover)
        self.player_guide_button = Button(SCREEN_WIDTH, SCREEN_HEIGHT*1.3, self.player_guide_img, self.screen, 0.75, self.player_guide_hover)
    
        run = True
        while run:
            self.screen.fill((52, 78, 91))
            
            if self.start_button.draw():
                self.ui = UI(data_parser, scorekeeper, data_fp, is_disable) #launch game ui if start button is clicked
            elif self.player_guide_button.draw():
                os.system("notepad.exe PlayerGuide.txt") # open player guide is player guide button is clicked
            
            GameMenu.draw_text(self, "Welcome to Dead or Alive! Click Start to begin:", font, TEXT_COL, 120, 200)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
            pygame.display.update()
        
        pygame.quit()
        
        
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
        
        
        
        