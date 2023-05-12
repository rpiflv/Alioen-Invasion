import sqlite3
import sys
import pygame
import sqlite3
from assets.settings import Settings
from assets.ship import Ship
from assets.bullet import Bullet
from assets.alien import Alien
from assets.game_stats import GameStats
from time import sleep
from assets.button import Button
from assets.scoreboard import Scoreboard

def provide_best3():
    best3 = []
    db = sqlite3.connect("highscores.sqlite")
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)")

    for name, score in cursor.execute("SELECT name, score FROM highscores ORDER BY score DESC LIMIT 3").fetchall():
        # best3.append(name, score)
        best3.append((name, score))
    cursor.close()
    db.commit()
    db.close()
    return best3

print(provide_best3()[1][0])