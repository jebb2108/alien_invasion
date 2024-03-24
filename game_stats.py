class GameStats():
    """ Отслеживание статистики для игры Alien Invasion. """

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_avtive = False

    def reset_stats(self):
        "Инициализирует статистику, изменяющиюся в ходе игры. "
        self.ship_left = self.settings.ship_limit
        self.score = 0