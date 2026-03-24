import pygame
import config
from core.game_state import GameState
from core.input_handler import InputHandler
from display.layout import Layout
from display.gem_animator import GemAnimator
from display.renderer import Renderer


def main():
    pygame.init()

    flags = pygame.FULLSCREEN if config.FULLSCREEN else 0
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags
    )
    pygame.display.set_caption('Daggerheart Fear Tracker')
    clock = pygame.time.Clock()

    state          = GameState()
    layout         = Layout()
    input_handler  = InputHandler()
    fear_anim      = GemAnimator(
        'assets/sprites/fear_gem.png',
        config.ANIM_APPEAR_FRAMES,
        config.GEM_NATIVE_SIZE,
    )
    hope_anim      = GemAnimator(
        'assets/sprites/hope_gem.png',
        config.ANIM_APPEAR_FRAMES,
        config.GEM_NATIVE_SIZE,
    )
    renderer       = Renderer(screen, layout, fear_anim, hope_anim)

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

        # ── Cap framerate ─────────────────────────────────────────────────────
        clock.tick(config.FPS)

        # ── Handle window close (laptop dev only) ─────────────────────────────
        for event in events:
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    main()
