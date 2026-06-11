import pygame
import config


class StartupMenu:
    def __init__(self, screen, font_small, font_large):
        self.screen = screen
        self.font_small = font_small
        self.font_large = font_large
        self.selected = 0  # 0: grayscale toggle, 1: hide_hope toggle, 2: start game
        self.grayscale = config.GRAYSCALE_MODE
        self.hide_hope = config.HIDE_HOPE

    def handle_input(self, events) -> bool:
        """
        Returns True when user confirms (press ENTER/SPACE to start game).
        Returns False to keep menu open.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % 3
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % 3
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.selected == 0:
                        self.grayscale = False
                    elif self.selected == 1:
                        self.hide_hope = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.selected == 0:
                        self.grayscale = True
                    elif self.selected == 1:
                        self.hide_hope = True
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.selected == 2:
                        return True
        return False

    def draw(self):
        self.screen.fill(config.COLOR_BG)

        title = self.font_large.render('Display Settings', True, config.COLOR_FEAR_TEXT)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 60))
        self.screen.blit(title, title_rect)

        y = 150
        row_height = 60

        for i in range(3):
            if i == 0:
                label = 'Grayscale Mode'
                value = 'ON' if self.grayscale else 'OFF'
            elif i == 1:
                label = 'Fear Only'
                value = 'ON' if self.hide_hope else 'OFF'
            else:
                label = 'Start Game'
                value = ''

            is_selected = (i == self.selected)
            text_color = config.COLOR_HOPE_TEXT if is_selected else config.COLOR_UI_MUTED

            label_surf = self.font_small.render(label, True, text_color)
            label_rect = label_surf.get_rect(center=(self.screen.get_width() // 2 - 100, y))
            self.screen.blit(label_surf, label_rect)

            if value:
                value_surf = self.font_small.render(value, True, text_color)
                value_rect = value_surf.get_rect(center=(self.screen.get_width() // 2 + 100, y))
                self.screen.blit(value_surf, value_rect)

            if is_selected:
                indicator = self.font_small.render('>', True, config.COLOR_FEAR_TEXT)
                indicator_rect = indicator.get_rect(center=(self.screen.get_width() // 2 - 200, y))
                self.screen.blit(indicator, indicator_rect)

            y += row_height

        hint_y = self.screen.get_height() - 50
        hint = self.font_small.render('↑↓ Navigate   ← → Toggle   [ENTER] Start', True, config.COLOR_UI_MUTED)
        hint_rect = hint.get_rect(center=(self.screen.get_width() // 2, hint_y))
        self.screen.blit(hint, hint_rect)
