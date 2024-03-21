class Settings:
    """ Класс для хранения всех настроек игры. """

    def __init__(self):
        """ Запуск игровых настроек. """
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Параметры корабля.
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Параметры снаряда.
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройки пришельцев.
        self.alien_speed = 1.0
        self.fleet_drop_speed = 100

        # Настройка 1 означает движение слева направо, а настройка -1 означает противоположное. 
        self.fleet_direction = 1