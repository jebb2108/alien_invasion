import json


class GameStats():
    """ Отслеживание статистики для игры Alien Invasion. """

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_avtive = False
        # Рекорд не должен сбрасываться.
        self.high_score = self.load_json()

    def reset_stats(self):
        "Инициализирует статистику, изменяющиюся в ходе игры. "
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    @staticmethod
    def load_json():
        filename = 'records.json'
        try:
            with open(filename) as f:
                record = f.read()
                return int(record)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                record = f.write('0')
                return int(record)
