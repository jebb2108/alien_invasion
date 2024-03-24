import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ Класс для управления ресурсами и поведением игры. """

    def __init__(self):
        """ Инициализирует игру и создает игровые ресурсы. """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        # и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self):
        """ Запуск основного цикла игры. """
        while True:
            self._check_events()
            
            if self.stats.game_avtive:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """ Отслеживание событий клавиатуры и мыши. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """ Реагирует на нажатие клавиш. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Событие на выход из игры.
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()            

    def _check_keyup_events(self, event):
        """ Реагирует на отпускание клавиш. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_play_button(self, mouse_pos):
        """ Запускает новую игру при нажатии кнопки Play. """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_avtive:
            # Сброс игровых настроек.
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_avtive = True
            self.sb.prep_score()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()


            # Создание нового флота.
            self._create_fleet()
            self.ship.center_ship()
            
            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """ Создает новый снаряд и добавляет его в группу. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Обновляет позиции снарядов и уничичтожает старые снаряды."""

        self.bullets.update()

        # Удаление снарядов вышедших за предел экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        """ Проверка попаданий в пришельцев. """
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # Уничтожает существующие снаряды и создает новый флот.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    
    def _check_aliens_bottom(self):
        """ Проверяет, добрались ли пришельцы до нижнего края экрана. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновениии с кораблем.
                self._ship_hit()
                break

    def _update_aliens(self):
        """ Обновление всех пришельцев во флоте. """
        """ Проверяет если флот находится у края экрана, то обновляет позицию флота."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """ Обрабатывает столкновение корабля с пришельцами. """
        if self.stats.ship_left > 0:
            # Уменьшение ship_left.
            self.stats.ship_left -= 1

        # Очистка списка пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

        # Пауза.
            sleep(0.5)

        else:
            self.stats.game_avtive = False
            pygame.mouse.set_visible(True)
    
    

    def _create_fleet(self):
        """ Создает флот пришельцев.  """
        # Создание пришельца и вычисление количества пришельцев в ряду.
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """ Создает прришельца и размещает его во флоте. """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """ Реагирует на достижение пришельцем края экрана. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Опускает весь флот и меняет направление флота. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """ Обновляет изображения на экране и рисует новый экран. """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Вывод информации о счете.
        self.sb.show_score()
        
        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_avtive:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    # Создает новый экземпляр и запускает игру.
    ai = AlienInvasion()
    ai.run_game()