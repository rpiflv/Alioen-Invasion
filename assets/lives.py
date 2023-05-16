import pygame
from pygame.sprite import Sprite


class Lives(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('assets/images/vaccine.png')
        self.life_image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.life_image.get_rect()
        # self.rect.bottomright = self.screen_rect.bottomright
        # self.rect.x = 900
        # self.rect.y = 900

        # self.x = float(self.rect.x)  # ship x position stored as a float

    # def blitme(self):
    #     self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x  # updating x position as a float

    def place_lives(self):
        self.rect.bottomright = self.screen_rect.bottomright
        self.x = self.rect.x
