import pygame
import config
from core.game_state import GameState
from core.input_handler import InputHandler
from display.layout import Layout
from display.gem_animator import GemAnimator
from display.renderer import Renderer
from display.menu import StartupMenu


def main():
    pygame.init()

    flags = pygame.FULLSCREEN if config.FULLSCREEN else (pygame.RESIZABLE if config.RESIZABLE else 0)
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags
    )
    pygame.display.set_caption('Daggerheart Fear Tracker')
    clock = pygame.time.Clock()

    font_small = _load_font(20)
    font_large = _load_font(48)

    # ── Show startup menu if enabled ───────────────────────────────────────────
    if config.SHOW_STARTUP_MENU:
        menu = StartupMenu(screen, font_small, font_large)
        menu_running = True
        while menu_running:
            events = pygame.event.get()
            menu_running = not menu.handle_input(events)
            menu.draw()
            pygame.display.flip()
            clock.tick(config.FPS)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            config.GRAYSCALE_MODE = menu.grayscale
            config.HIDE_HOPE = menu.hide_hope
            # Re-evaluate colors now that mode has changed
            _update_colors()

    state         = GameState()
    layout        = Layout(*screen.get_size())
    input_handler = InputHandler()
    fear_anim     = GemAnimator(
        'assets/sprites/fear_gem.png',
        config.ANIM_APPEAR_FRAMES,
        config.GEM_NATIVE_SIZE,
    )
    hope_anim     = GemAnimator(
        'assets/sprites/hope_gem.png',
        config.ANIM_APPEAR_FRAMES,
        config.GEM_NATIVE_SIZE,
    )
    renderer      = Renderer(screen, layout, fear_anim, hope_anim)

    running = True
    while running:
        events  = pygame.event.get()
        actions = input_handler.get_actions(events)

        # ── Process actions ───────────────────────────────────────────────────
        for action in actions:
            if   action == 'FEAR_ADD':      state.add_fear()
            elif action == 'FEAR_SUBTRACT': state.subtract_fear()
            elif action == 'HOPE_ADD':      state.add_hope()
            elif action == 'HOPE_SUBTRACT': state.subtract_hope()
            elif action == 'RESET':         state.reset()
            elif action == 'QUIT':          running = False

        # ── Trigger animations if state changed ───────────────────────────────
        delta = state.consume_fear_delta()
        if   delta == +1: fear_anim.trigger_appear()
        elif delta == -1: fear_anim.trigger_vanish()

        delta = state.consume_hope_delta()
        if   delta == +1: hope_anim.trigger_appear()
        elif delta == -1: hope_anim.trigger_vanish()

        # ── Update animation state ────────────────────────────────────────────
        now = pygame.time.get_ticks()
        fear_anim.update(now)
        hope_anim.update(now)

        # ── Draw ──────────────────────────────────────────────────────────────
        renderer.draw(state)
        pygame.display.flip()

        # ── Cap framerate ─────────────────────────────────────────────────────
        clock.tick(config.FPS)

        # ── Handle window close and resize ────────────────────────────────────
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.WINDOWRESIZED:
                layout           = Layout(event.x, event.y)
                renderer.layout  = layout

    pygame.quit()


def _load_font(size: int) -> pygame.font.Font:
    import os
    font_path = os.path.join('assets', 'fonts', 'pixel_font.ttf')
    if os.path.exists(font_path):
        return pygame.font.Font(font_path, size)
    return pygame.font.SysFont('monospace', size)


def _update_colors():
    """Re-evaluate color constants based on current display mode settings."""
    config.COLOR_BG = (
        (0, 0, 0) if config.GRAYSCALE_MODE else (18, 10, 30)
    )
    config.COLOR_FEAR_TEXT = (
        (125, 125, 125) if config.GRAYSCALE_MODE else (174, 232, 4)
    )
    config.COLOR_HOPE_TEXT = (
        (225, 225, 225) if config.GRAYSCALE_MODE else (50, 150, 200)
    )
    config.COLOR_UI_MUTED = (
        (170, 170, 170) if config.GRAYSCALE_MODE else (122, 107, 138)
    )


if __name__ == '__main__':
    main()
