import sqlite3


class HighScores:
    def __init__(self, ai_game):
        self.stats = ai_game.stats
        self.highest_score = 0
        # self._provide_highscore()

    # def _provide_highscore(self):
    #
    #     db = sqlite3.connect("highscores.sqlite")
    #     cursor = db.cursor()
    #
    #     cursor.execute("CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)")
    #     db.execute('INSERT INTO highscores VALUES (name = ?, score = ?)')
    #     # db.execute('INSERT INTO highscores VALUES ("ANG", 1500000)')
    #     # db.execute('INSERT INTO highscores VALUES ("KAL", 500000)')
    #
    #     for name, score in cursor.execute("SELECT name, MAX(score)  FROM highscores").fetchall():
    #     # self.stats.score = self.highest_score
    #         return name, score
    #
    #     cursor.close()
    #     db.commit()
    #     db.close()


# current_high = HighScores()

# print(current_high._provide_highscore())


    # def add_high_score(self, name, new_high, ai_game):
    #
    #     self.name = input("Please enter your name ").capitalize()
    #     self.new_high = ai_game.stats.score
    #     db = sqlite3.connect("highscores.sqlite")
    #     db.execute('INSERT INTO highscores VALUES ({name}, {self.stats.high_score[1]})')

# new_high = HighScores()
# new_high.add_high_score("flav", 1750)
