import tkinter as tk
import os
import pygame

class Button():
    def __init__(self, w, h, image, screen, scale, imagehover):
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = [(w / 2) - int(self.width * scale) / 2, (h / 2) - int(self.height * scale) / 2]
        self.screen = screen
        self.clicked = False
        self.imagehover = pygame.transform.scale(imagehover, (int(self.width * scale * 1.2), int(self.height * scale * 1.2)))
    
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #gets top left coordinates of the button image when hovered over
        x = self.rect.topleft[0] - (int(self.width * self.scale * 1.2) - int(self.width * self.scale)) / 2
        y = self.rect.topleft[1] - (int(self.height * self.scale * 1.2) - int(self.height * self.scale)) / 2
        
        #draw button on screen
        self.screen.blit(self.image, (self.rect.topleft[0], self.rect.topleft[1]))
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.screen.blit(self.imagehover, (x, y)) #changes button image when hovered over
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
                
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
        
        return action
        


