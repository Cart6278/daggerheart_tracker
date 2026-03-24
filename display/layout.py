import config


class Layout:
    def __init__(self):
        w, h = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        pad  = config.GEM_DISPLAY_SIZE          # One gem-width used as padding unit
        half = w // 2

        # ── Labels ────────────────────────────────────────────────────────────
        # Sit near the top of each half, horizontally centred
        self.fear_label_pos = (half // 2,          30)
        self.hope_label_pos = (half + half // 2,   30)

        # ── Counters ──────────────────────────────────────────────────────────
        # Large numeric display, below the label
        self.fear_counter_pos = (half // 2,        80)
        self.hope_counter_pos = (half + half // 2, 80)

        # ── Gem grid origins ──────────────────────────────────────────────────
        # Top-left corner of the first gem slot in each grid.
        # Grids are horizontally centred within their half of the screen.
        self.gem_cols = 6   # Gems per row before wrapping to a new row
        grid_w        = self.gem_cols * pad
        fear_x        = (half - grid_w) // 2
        hope_x        = half + (half - grid_w) // 2
        grid_y        = h // 2 - pad // 2   # Vertically centred in lower portion

        self.fear_grid_origin = (fear_x, grid_y)
        self.hope_grid_origin = (hope_x, grid_y)

        # ── Hint text ─────────────────────────────────────────────────────────
        # Button reminder at the bottom centre of the screen
        self.hint_pos = (w // 2, h - 20)

        # ── Divider ───────────────────────────────────────────────────────────
        # Centre line separating Fear and Hope halves
        self.divider_x = half

    # ── Gem position helpers ──────────────────────────────────────────────────

    def gem_position(self, gem_type: str, index: int) -> tuple[int, int]:
        """
        Returns the (x, y) top-left pixel position for gem slot [index]
        in the given grid ('fear' or 'hope').

        Slots fill left-to-right, wrapping after gem_cols columns.
        """
        origin = self.fear_grid_origin if gem_type == 'fear' else self.hope_grid_origin
        col    = index % self.gem_cols
        row    = index // self.gem_cols
        size   = config.GEM_DISPLAY_SIZE
        x      = origin[0] + col * size
        y      = origin[1] + row * size
        return (x, y)

    def animated_gem_index(self, count: int, delta: int) -> int:
        """
        Returns the slot index that should run an animation this frame.

        - On appear  (delta == +1): the slot just filled   → index count - 1
        - On vanish  (delta == -1): the slot just emptied  → index count
        - No change  (delta ==  0): returns -1 (no animation)
        """
        if delta == +1:
            return count - 1   # Rightmost filled slot
        if delta == -1:
            return count       # Slot just vacated
        return -1

    def gem_slot_rects(self, gem_type: str) -> list[tuple[int, int]]:
        """
        Returns a list of (x, y) positions for every slot in the grid,
        ordered left-to-right, top-to-bottom.

        Total slots = FEAR_MAX (or HOPE_MAX) — both share the same maximum.
        """
        max_gems = config.FEAR_MAX if gem_type == 'fear' else config.HOPE_MAX
        return [self.gem_position(gem_type, i) for i in range(max_gems)]
