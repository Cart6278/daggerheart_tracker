import pygame
import config


class InputHandler:
    def __init__(self):
        if config.USE_GPIO:
            self._setup_gpio()

    def get_actions(self, pygame_events) -> list[str]:
        """
        Returns a list of action strings for this frame.
        e.g. ['FEAR_ADD'] or ['HOPE_SUBTRACT', 'RESET']
        Called once per frame from the main loop.
        """
        if config.USE_GPIO:
            return self._read_gpio()
        return self._read_keyboard(pygame_events)

    # ── Keyboard (development / laptop) ───────────────────────────────────────
    def _read_keyboard(self, events) -> list[str]:
        key_map = {
            getattr(pygame, f'K_{config.KEY_FEAR_ADD}',      pygame.K_UP):    'FEAR_ADD',
            getattr(pygame, f'K_{config.KEY_FEAR_SUBTRACT}', pygame.K_DOWN):  'FEAR_SUBTRACT',
            getattr(pygame, f'K_{config.KEY_HOPE_ADD}',      pygame.K_RIGHT): 'HOPE_ADD',
            getattr(pygame, f'K_{config.KEY_HOPE_SUBTRACT}', pygame.K_LEFT):  'HOPE_SUBTRACT',
            getattr(pygame, f'K_{config.KEY_RESET}',         pygame.K_r):     'RESET',
            getattr(pygame, f'K_{config.KEY_QUIT}',          pygame.K_q):     'QUIT',
            # WASD alternatives
            pygame.K_w: 'FEAR_ADD',
            pygame.K_s: 'FEAR_SUBTRACT',
            pygame.K_d: 'HOPE_ADD',
            pygame.K_a: 'HOPE_SUBTRACT',
        }

        actions = []
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in key_map:
                actions.append(key_map[event.key])
        return actions

    # ── GPIO (Raspberry Pi hardware) ──────────────────────────────────────────
    def _setup_gpio(self):
        import RPi.GPIO as GPIO
        self._GPIO = GPIO
        self._last_states = {}

        GPIO.setmode(GPIO.BCM)
        for pin in self._gpio_pin_map().keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self._last_states[pin] = GPIO.HIGH  # Unpressed (active low)

    def _read_gpio(self) -> list[str]:
        actions = []
        for pin, action in self._gpio_pin_map().items():
            current = self._GPIO.input(pin)
            if current == self._GPIO.LOW and self._last_states[pin] == self._GPIO.HIGH:
                actions.append(action)
            self._last_states[pin] = current
        return actions

    def _gpio_pin_map(self) -> dict[int, str]:
        return {
            config.GPIO_FEAR_ADD:      'FEAR_ADD',
            config.GPIO_FEAR_SUBTRACT: 'FEAR_SUBTRACT',
            config.GPIO_HOPE_ADD:      'HOPE_ADD',
            config.GPIO_HOPE_SUBTRACT: 'HOPE_SUBTRACT',
            config.GPIO_RESET:         'RESET',
            config.GPIO_QUIT:          'QUIT',
        }
