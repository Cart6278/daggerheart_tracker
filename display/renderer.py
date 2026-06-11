import os
import pygame
import config


# ── Fallback colors for when sprite assets are not yet available ──────────────
_COLOR_FEAR_GEM_FILLED  = config.COLOR_FEAR_TEXT          # Gold
_COLOR_HOPE_GEM_FILLED  = config.COLOR_HOPE_TEXT          # Teal
_COLOR_GEM_EMPTY        = ( 40,  34,  52)                 # Very dark purple
_COLOR_GEM_EMPTY_BORDER = ( 80,  68, 100)                 # Muted purple outline
_COLOR_DIVIDER          = ( 50,  40,  70)                 # Subtle divider line
_COLOR_FLASH            = (255, 255, 255)                  # Counter flash white

# How many frames the counter flashes white after a change
_FLASH_FRAME_COUNT = 2


class Renderer:
    def __init__(self, screen, layout, fear_animator, hope_animator):
        self.screen     = screen
        self.layout     = layout
        self.fear_anim  = fear_animator
        self.hope_anim  = hope_animator

        self.font_large = self._load_font(48)
        self.font_small = self._load_font(20)

        # Flash counters — count down from _FLASH_FRAME_COUNT to 0
        self._fear_flash = 0
        self._hope_flash = 0

    # ── Public ────────────────────────────────────────────────────────────────

    def draw(self, game_state):
        self.screen.fill(config.COLOR_BG)
        if not config.HIDE_HOPE:
            self._draw_divider()
        self._draw_labels()
        self._update_flash(game_state)
        self._draw_counters(game_state)
        self._draw_gem_grid('fear', game_state.fear, self.fear_anim)
        if not config.HIDE_HOPE:
            self._draw_gem_grid('hope', game_state.hope, self.hope_anim)
        self._draw_hints()

    # ── Layout elements ───────────────────────────────────────────────────────

    def _draw_divider(self):
        x = self.layout.divider_x
        pygame.draw.line(
            self.screen,
            _COLOR_DIVIDER,
            (x, self.layout.divider_top),
            (x, self.layout.divider_bottom),
            1,
        )

    def _draw_labels(self):
        fear_surf = self.font_small.render('F E A R', True, config.COLOR_FEAR_TEXT)
        self._blit_centred(fear_surf, self.layout.fear_label_pos)
        if not config.HIDE_HOPE:
            hope_surf = self.font_small.render('H O P E', True, config.COLOR_HOPE_TEXT)
            self._blit_centred(hope_surf, self.layout.hope_label_pos)

    def _update_flash(self, game_state):
        if game_state.fear_changed:
            self._fear_flash = _FLASH_FRAME_COUNT
        if game_state.hope_changed:
            self._hope_flash = _FLASH_FRAME_COUNT

    def _draw_counters(self, game_state):
        fear_color = _COLOR_FLASH if self._fear_flash > 0 else config.COLOR_FEAR_TEXT
        hope_color = _COLOR_FLASH if self._hope_flash > 0 else config.COLOR_HOPE_TEXT

        fear_surf = self.font_large.render(str(game_state.fear), True, fear_color)
        hope_surf = self.font_large.render(str(game_state.hope), True, hope_color)
        self._blit_centred(fear_surf, self.layout.fear_counter_pos)
        self._blit_centred(hope_surf, self.layout.hope_counter_pos)

        if self._fear_flash > 0:
            self._fear_flash -= 1
        if self._hope_flash > 0:
            self._hope_flash -= 1

    def _draw_hints(self):
        if config.HIDE_HOPE:
            hint_text = '\u2191/\u2193 Fear   [R] Reset   [Q] Quit'
        else:
            hint_text = '\u2191/\u2193 Fear   \u2192/\u2190 Hope   [R] Reset   [Q] Quit'
        hint = self.font_small.render(hint_text, True, config.COLOR_UI_MUTED)
        self._blit_centred(hint, self.layout.hint_pos)

    # ── Gem grid ──────────────────────────────────────────────────────────────

    def _draw_gem_grid(self, gem_type, count, animator):
        max_gems      = config.FEAR_MAX if gem_type == 'fear' else config.HOPE_MAX
        anim_index    = self.layout.animated_gem_index(count, animator.pending_delta)
        filled_color  = _COLOR_FEAR_GEM_FILLED if gem_type == 'fear' else _COLOR_HOPE_GEM_FILLED

        for i in range(max_gems):
            pos     = self.layout.gem_position(gem_type, i)
            is_anim = (i == anim_index and animator.state != 'idle')

            if is_anim:
                self._draw_animated_gem(pos, animator)
            elif i < count:
                self._draw_filled_gem(pos, filled_color)
            else:
                self._draw_empty_slot(pos)

    def _draw_animated_gem(self, pos, animator):
        surface = animator.get_current_surface()
        if surface:
            self.screen.blit(surface, pos)
        # If the animator has no surface yet (no sprite sheet loaded),
        # nothing is drawn — the slot briefly shows as empty during animation.

    def _draw_filled_gem(self, pos, color):
        surface = self._make_gem_surface(color, filled=True)
        self.screen.blit(surface, pos)

    def _draw_empty_slot(self, pos):
        surface = self._make_gem_surface(_COLOR_GEM_EMPTY, filled=False)
        self.screen.blit(surface, pos)

    # ── Gem shape primitives ──────────────────────────────────────────────────

    def _make_gem_surface(self, color, filled: bool) -> pygame.Surface:
        """
        Draws a diamond (rotated square) gem shape onto a transparent surface.
        Used as a fallback when sprite sheet assets are not yet available.
        When sprite sheets exist the animator's get_current_surface() replaces this
        for animated slots, but static filled/empty slots will still use this
        until per-slot sprite support is added.
        """
        size    = self.layout.gem_size
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy  = size // 2, size // 2
        margin  = size // 6

        points = [
            (cx,          margin),        # top
            (size - margin, cy),          # right
            (cx,          size - margin), # bottom
            (margin,      cy),            # left
        ]

        if filled:
            pygame.draw.polygon(surface, color, points)
            # Inner highlight — small bright centre point for depth
            highlight = tuple(min(c + 60, 255) for c in color)
            inner = size // 5
            inner_pts = [
                (cx,           cy - inner),
                (cx + inner,   cy),
                (cx,           cy + inner),
                (cx - inner,   cy),
            ]
            pygame.draw.polygon(surface, highlight, inner_pts)
        else:
            pygame.draw.polygon(surface, _COLOR_GEM_EMPTY_BORDER, points, 1)

        return surface

    # ── Utilities ─────────────────────────────────────────────────────────────

    def _blit_centred(self, surface, centre_pos):
        rect = surface.get_rect(center=centre_pos)
        self.screen.blit(surface, rect)

    @staticmethod
    def _load_font(size: int) -> pygame.font.Font:
        font_path = os.path.join('assets', 'fonts', 'pixel_font.ttf')
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
        return pygame.font.SysFont('monospace', size)
