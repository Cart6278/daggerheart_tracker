import os
import pygame
import config


class GemAnimator:
    def __init__(self, sprite_sheet_path: str, frame_count: int, frame_size: int):
        self.state         = 'idle'  # 'idle' | 'appearing' | 'vanishing'
        self.frame_idx     = 0
        self.pending_delta = 0       # +1 while appearing, -1 while vanishing, 0 when idle
        self._last_tick    = 0

        self.frames_scaled = self._load(sprite_sheet_path, frame_count, frame_size)

    # ── Triggers ──────────────────────────────────────────────────────────────

    def trigger_appear(self):
        self.state         = 'appearing'
        self.frame_idx     = 0
        self.pending_delta = +1
        self._last_tick    = 0

    def trigger_vanish(self):
        self.state         = 'vanishing'
        self.frame_idx     = max(0, len(self.frames_scaled) - 1)  # Play backwards
        self.pending_delta = -1
        self._last_tick    = 0

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, current_time_ms: int):
        """Advance one animation frame if enough time has passed. Call once per game loop tick."""
        if self.state == 'idle':
            return
        if current_time_ms - self._last_tick >= config.ANIM_FRAME_DURATION:
            self._advance_frame()
            self._last_tick = current_time_ms

    # ── Surface ───────────────────────────────────────────────────────────────

    def get_current_surface(self) -> pygame.Surface | None:
        """
        Returns the scaled Pygame surface for the current animation frame.
        Returns None if no sprite sheet is loaded — the renderer falls back
        to its built-in gem shape drawing in that case.
        """
        if not self.frames_scaled:
            return None
        idx = max(0, min(self.frame_idx, len(self.frames_scaled) - 1))
        return self.frames_scaled[idx]

    # ── Internal ──────────────────────────────────────────────────────────────

    def _advance_frame(self):
        if self.state == 'appearing':
            self.frame_idx += 1
            if self.frame_idx >= len(self.frames_scaled):
                self.frame_idx     = max(0, len(self.frames_scaled) - 1)
                self.state         = 'idle'
                self.pending_delta = 0

        elif self.state == 'vanishing':
            self.frame_idx -= 1
            if self.frame_idx < 0:
                self.frame_idx     = 0
                self.state         = 'idle'
                self.pending_delta = 0

    def _load(
        self, path: str, frame_count: int, frame_size: int
    ) -> list[pygame.Surface]:
        """
        Loads a sprite sheet and returns a list of scaled surfaces, one per frame.
        Frames are assumed to be laid out left-to-right in a single row.

        If the file does not exist the animator runs without sprites — all
        get_current_surface() calls return None and the renderer draws its
        fallback gem shapes instead.
        """
        if not os.path.exists(path):
            return []

        sheet  = pygame.image.load(path).convert_alpha()
        frames = [
            sheet.subsurface((i * frame_size, 0, frame_size, frame_size))
            for i in range(frame_count)
        ]
        scaled = [
            pygame.transform.scale(f, (config.GEM_DISPLAY_SIZE, config.GEM_DISPLAY_SIZE))
            for f in frames
        ]
        return scaled
