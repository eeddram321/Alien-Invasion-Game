import pygame
from pygame.sprite import Sprite

class Rock(Sprite):
    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('Images/Rocks_small.png')
        self.rect = self.image.get_rect()

        #start each rock near the top right corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #store rocks exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        '''Return True if rock is at edge of screen'''
        screen_rect = self.screen.get_rect()
        return(self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    
    def update(self):
        '''Move the rock to the right'''
        self.x += self.settings.rock_speed * self.settings.rock_fleet_direction
        self.rect.x = self.x

       




