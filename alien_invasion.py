import sys
import pygame
import sqlite3
from assets.settings import Settings
from assets.ship import Ship
from assets.bullet import Bullet
from assets.alien import Alien
from assets.lives import Lives
from assets.game_stats import GameStats
from time import sleep
from assets.button import Button
from assets.scoreboard import Scoreboard
import random


class AlienInvasion:
    """Overall class to manage the app"""

    def __init__(self):

        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # full screen mode
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)  # self-> ai_game
        self.lives = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.stats = GameStats(self)
        self._create_lives_left(self.settings.ship_limit)

        self.play_button = Button(self, "Play")
        self.scoreboard = Scoreboard(self)


        self.stars = []
        self.star_pos = []
        self.star_y_float = []

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - ( 2 * alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_of_aliens_in_row = available_space_x // (2 * alien_width)

        number_of_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_in_row):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _create_lives_left(self, ships_left):
        for ship_number in range(ships_left):
            print(ships_left)
            self._create_life(ship_number)

    def _create_life(self, ship_number):
        life = Lives(self)
        life_width, life_height = life.rect.size
        life.x = life_width + 2 * life_width * ship_number
        # life.rect.x = self.settings.screen_width - 2 * life.x
        life.rect.x = life.x
        life.rect.y = self.settings.screen_height - life_height
        self.lives.add(life)

    def _check_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.provide_highscore()
            self.scoreboard._prep_score()
            self.scoreboard._prep_level()
            self.scoreboard._prep_high_score()
            pygame.mouse.set_visible(False)

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.scoreboard.show()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            self.stats.score += self.settings.alien_score
            # self.scoreboard.check_high_score()
            self.scoreboard._prep_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard._prep_level()
            # self.settings.alien_speed += 0.1

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
             self._ship_hit()
        self._check_alien_bottom()

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings._fleet_drop_speed
        self.settings.fleet_direction *= -1

    def populate_bg(self):
        for i in range(0, 50):
            rand_x = random.randint(1, 1200)
            rand_y = random.randint(1, 800)
            self.star_pos.append((rand_x, rand_y))
            self.star_y = self.star_pos[i][1]
            self.star_rect = pygame.Rect(self.star_pos[i][0], self.star_y, self.settings.STAR_WIDTH, self.settings.STAR_WIDTH)
            self.stars.append(self.star_rect)
            self.star_y_float.append(float(self.star_y))

        for i in range(0, 7):
            rand_x = random.randint(1, 1200)
            rand_y = random.randint(1, 800)
            self.star_pos.append((rand_x, rand_y))
            self.star_y = self.star_pos[i][1]
            self.big_star_rect = pygame.Rect(self.star_pos[i][0], self.star_y, self.settings.BIG_STAR_WIDTH, self.settings.BIG_STAR_WIDTH)
            self.stars.append(self.big_star_rect)
            self.star_y_float.append(float(self.star_y))

    def update_stars(self):
        for i in range(len(self.stars)):
            pygame.draw.rect(self.screen, (255, 255, 255), self.stars[i])
            self.star_y_float[i] += self.settings.STAR_SPEED
            self.stars[i].y = self.star_y_float[i]

            if self.star_y_float[i] > self.settings.screen_height:
                self.star_y_float[i] = 0

    def _fire_bullet(self):
        if len(self.bullets) <= self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.update_stars()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.lives.draw(self.screen)
        self.ship.blitme()
        self.scoreboard.show()
        if not self.stats.game_active:
            self.play_button._draw_button()
        pygame.display.flip()

    def _ship_hit(self):
        # To keep playing in case you still have ships, or new run.
        # In case of high score, store it.
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self.lives.empty()
            self._create_fleet()
            self._create_lives_left(self.stats.ships_left)
            self.ship.center_ship()

            sleep(1.5)
        else:
            if self.stats.score > self.stats.high_score[1]:
                self.add_high_score()
                self.stats.high_score = self.name, self.new_high
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def provide_highscore(self):

        db = sqlite3.connect("highscores.sqlite")
        cursor = db.cursor()
        result = None
        cursor.execute("CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)")

        for name, score in cursor.execute("SELECT name, MAX(score)  FROM highscores").fetchall():
            result = name, score
        cursor.close()
        db.commit()
        db.close()
        return result

    def add_high_score(self):
        # addinmg high score to the DB
        db = sqlite3.connect("highscores.sqlite")
        self.new_high = self.stats.score
        self.scoreboard._prep_high_score()
        self.name = self.input_name()
        add_sql = 'INSERT INTO highscores VALUES (?, ?)'
        db.execute(add_sql, (self.name, self.new_high))
        cursor = db.cursor()
        cursor.execute("DELETE FROM highscores WHERE SCORE in (SELECT score FROM highscores ORDER BY score ASC LIMIT 1)")
        db.commit()
        db.close()

    def provide_best3(self):
        best3 = []
        db = sqlite3.connect("highscores.sqlite")
        cursor = db.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)")

        for name, score in cursor.execute("SELECT name, score FROM highscores ORDER BY score DESC LIMIT 3").fetchall():
            best3.append((name, score))
        cursor.close()
        db.commit()
        db.close()
        return best3

    def input_name(self):
        rect = pygame.Rect(200, 200, 300, 200)
        FONT_TITLE = pygame.font.Font("images/ZenDots-Regular.ttf", 50)
        FONT_NAME = pygame.font.Font("images/ZenDots-Regular.ttf", 50)
        FONT_LIST = pygame.font.Font("images/ZenDots-Regular.ttf", 37)
        input_rect = pygame.Rect(rect.y + 10, rect.x + 10, rect.width - 20, rect.height - 140)
        rect_2 = pygame.Rect(700, 200, 350, 300)
        text = ''.upper()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            self.screen.fill((30, 30, 30))
            high_score_surface_current = FONT_NAME.render(f"{self.stats.score}", True, (255, 255, 255))
            high_score_surface_first = FONT_LIST.render(f"1. {self.provide_best3()[0][0]}, "
                                                        f" {self.provide_best3()[0][1]}", True, (195, 195, 195))
            high_score_surface_second = FONT_LIST.render(f"2. {str(self.provide_best3()[1][0])},"
                                                         f" {str(self.provide_best3()[1][1])}", True, (195, 195, 195))
            high_score_surface_third = FONT_LIST.render(f"3. {str(self.provide_best3()[2][0])}, "
                                                        f"{str(self.provide_best3()[2][1])}", True, (195, 195, 195))
            title_surface = FONT_TITLE.render('Enter your name:', True, (195, 195, 195))
            text_surface = FONT_NAME.render(text, True, (255, 255, 255))

            high_score_surface_current_rect = high_score_surface_current.get_rect()
            high_score_surface_current_rect.y = input_rect.y + 100
            high_score_surface_current_rect.x = input_rect.x

            high_score_surface_first_rect = high_score_surface_first.get_rect()
            high_score_surface_first_rect.y = rect_2.y + 10
            high_score_surface_first_rect.x = rect_2.x + 10

            high_score_surface_second_rect = high_score_surface_second.get_rect()
            high_score_surface_second_rect.y = high_score_surface_first_rect.y + 100
            high_score_surface_second_rect.x = rect_2.x + 10

            high_score_surface_third_rect = high_score_surface_third.get_rect()
            high_score_surface_third_rect.y = high_score_surface_second_rect.y + 100
            high_score_surface_third_rect.x = rect_2.x + 10

            title_surface_rect = title_surface.get_rect()
            title_surface_rect.y = rect.y - 100
            title_surface_rect.x = rect.x + 45

            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            pygame.draw.rect(self.screen, (255, 255, 255), rect_2, 2)
            pygame.draw.rect(self.screen, (255, 0, 255), input_rect, 2)

            self.screen.blit(title_surface, title_surface_rect)
            self.screen.blit(text_surface, input_rect)
            self.screen.blit(high_score_surface_first, high_score_surface_first_rect)
            self.screen.blit(high_score_surface_second, high_score_surface_second_rect)
            self.screen.blit(high_score_surface_third, high_score_surface_third_rect)
            self.screen.blit(high_score_surface_current, high_score_surface_current_rect)
            pygame.display.flip()

    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit() # same behaviour as ship hit
                break

    def run_game(self):
        """Start the MAIN LOOP"""
        self.populate_bg()
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self.update_screen()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
