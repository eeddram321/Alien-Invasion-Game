import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        

        #Load the star image and set its rect attribute
        self.image = pygame.image.load('Images/Blue_star.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)