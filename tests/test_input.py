from unittest.mock import MagicMock, patch
import config


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_keydown_event(key):
    """Returns a mock pygame KEYDOWN event for the given key constant."""
    event = MagicMock()
    event.type = 768   # pygame.KEYDOWN constant
    event.key  = key
    return event


def make_handler():
    """Returns an InputHandler with USE_GPIO forced off."""
    with patch.object(config, 'USE_GPIO', False):
        from core.input_handler import InputHandler
        return InputHandler()


# ── Keyboard: action mapping ───────────────────────────────────────────────────

def test_up_arrow_maps_to_fear_add():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_UP)]
    assert 'FEAR_ADD' in handler.get_actions(events)
    pygame.quit()

def test_down_arrow_maps_to_fear_subtract():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_DOWN)]
    assert 'FEAR_SUBTRACT' in handler.get_actions(events)
    pygame.quit()

def test_right_arrow_maps_to_hope_add():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_RIGHT)]
    assert 'HOPE_ADD' in handler.get_actions(events)
    pygame.quit()

def test_left_arrow_maps_to_hope_subtract():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_LEFT)]
    assert 'HOPE_SUBTRACT' in handler.get_actions(events)
    pygame.quit()

def test_r_key_maps_to_reset():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_r)]
    assert 'RESET' in handler.get_actions(events)
    pygame.quit()

def test_q_key_maps_to_quit():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_q)]
    assert 'QUIT' in handler.get_actions(events)
    pygame.quit()


# ── Keyboard: edge cases ──────────────────────────────────────────────────────

def test_no_events_returns_empty_list():
    import pygame
    pygame.init()
    handler = make_handler()
    assert handler.get_actions([]) == []
    pygame.quit()

def test_unbound_key_returns_no_action():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_z)]
    assert handler.get_actions(events) == []
    pygame.quit()

def test_multiple_keys_return_multiple_actions():
    import pygame
    pygame.init()
    handler = make_handler()
    events  = [make_keydown_event(pygame.K_UP), make_keydown_event(pygame.K_RIGHT)]
    actions = handler.get_actions(events)
    assert 'FEAR_ADD' in actions
    assert 'HOPE_ADD' in actions
    pygame.quit()

def test_non_keydown_event_ignored():
    import pygame
    pygame.init()
    handler       = make_handler()
    event         = MagicMock()
    event.type    = 769   # pygame.KEYUP constant — should be ignored
    event.key     = pygame.K_UP
    assert handler.get_actions([event]) == []
    pygame.quit()


# ── GPIO: pin map ─────────────────────────────────────────────────────────────

def test_gpio_pin_map_contains_all_actions():
    with patch.object(config, 'USE_GPIO', False):
        from core.input_handler import InputHandler
        handler  = InputHandler()
        pin_map  = handler._gpio_pin_map()
        expected = {'FEAR_ADD', 'FEAR_SUBTRACT', 'HOPE_ADD', 'HOPE_SUBTRACT', 'RESET', 'QUIT'}
        assert set(pin_map.values()) == expected

def test_gpio_pin_map_uses_config_pins():
    with patch.object(config, 'USE_GPIO', False):
        from core.input_handler import InputHandler
        handler = InputHandler()
        pin_map = handler._gpio_pin_map()
        assert config.GPIO_FEAR_ADD      in pin_map
        assert config.GPIO_FEAR_SUBTRACT in pin_map
        assert config.GPIO_HOPE_ADD      in pin_map
        assert config.GPIO_HOPE_SUBTRACT in pin_map
        assert config.GPIO_RESET         in pin_map
        assert config.GPIO_QUIT          in pin_map
