import pygame
import os
# syringe = os.path.abspath('assets/images/syringe.png')
syringe = os.path.relpath('assets/images/syringe.png')

class Ship:
    """A class to manage ships"""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.moving_right = False  # FLAG
        self.moving_left = False
        self.settings = ai_game.settings

        self.image = pygame.image.load(syringe)
        self.rect = self.image.get_rect()
        # self.life = pygame.transform.scale(self.image, (20, 40))
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # ship x position stored as a float

    def blitme(self):
        """Draw the ship in the current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x  # updating x position as a float

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
