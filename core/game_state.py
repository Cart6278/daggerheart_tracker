import config


class GameState:
    def __init__(self):
        self.fear = 0
        self.hope = 0
        self._last_fear_delta = 0  # +1 or -1, used to trigger correct animation
        self._last_hope_delta = 0

    # ── Fear ──────────────────────────────────────────────────────────────────
    def add_fear(self):
        if self.fear < config.FEAR_MAX:
            self.fear += 1
            self._last_fear_delta = +1

    def subtract_fear(self):
        if self.fear > config.FEAR_MIN:
            self.fear -= 1
            self._last_fear_delta = -1

    # ── Hope ──────────────────────────────────────────────────────────────────
    def add_hope(self):
        if self.hope < config.HOPE_MAX:
            self.hope += 1
            self._last_hope_delta = +1

    def subtract_hope(self):
        if self.hope > config.HOPE_MIN:
            self.hope -= 1
            self._last_hope_delta = -1

    # ── Reset ─────────────────────────────────────────────────────────────────
    def reset(self):
        self.fear = 0
        self.hope = 0
        self._last_fear_delta = 0
        self._last_hope_delta = 0

    # ── Read-only properties ──────────────────────────────────────────────────
    @property
    def fear_changed(self):
        return self._last_fear_delta != 0

    @property
    def hope_changed(self):
        return self._last_hope_delta != 0

    def consume_fear_delta(self):
        delta = self._last_fear_delta
        self._last_fear_delta = 0
        return delta  # +1 triggers appear anim, -1 triggers vanish anim

    def consume_hope_delta(self):
        delta = self._last_hope_delta
        self._last_hope_delta = 0
        return delta  # +1 triggers appear anim, -1 triggers vanish anim
