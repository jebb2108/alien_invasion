import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ Класс для управления кораблем. """

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его изначальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохраняется вещественные координаты центра корабля.
        self.x = float(self.rect.x)

        # Флажки для движения; начинает с корабля, который не двигается.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию корабля в соответствии с состоянием флажков."""
        # Обновляется атрибут Х, а не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        # Обновляет пряумогольный объект от self.x.
        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Размещает корабль в центре нижней стороны. """
        self.rect.midbottom = self.screen_rect.midbottom 
        self.x = float(self.rect.x)