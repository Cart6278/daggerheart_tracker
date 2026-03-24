from core.game_state import GameState


# ── Fear ──────────────────────────────────────────────────────────────────────

def test_fear_starts_at_zero():
    assert GameState().fear == 0

def test_fear_increments():
    state = GameState()
    state.add_fear()
    assert state.fear == 1

def test_fear_decrements():
    state = GameState()
    state.add_fear()
    state.add_fear()
    state.subtract_fear()
    assert state.fear == 1

def test_fear_does_not_exceed_max():
    state = GameState()
    for _ in range(20):
        state.add_fear()
    assert state.fear == 12  # FEAR_MAX

def test_fear_does_not_go_below_min():
    state = GameState()
    state.subtract_fear()
    assert state.fear == 0  # FEAR_MIN

def test_fear_add_sets_positive_delta():
    state = GameState()
    state.add_fear()
    assert state._last_fear_delta == +1

def test_fear_subtract_sets_negative_delta():
    state = GameState()
    state.add_fear()
    state.consume_fear_delta()
    state.subtract_fear()
    assert state._last_fear_delta == -1

def test_fear_at_max_does_not_set_delta():
    state = GameState()
    for _ in range(12):
        state.add_fear()
    state.consume_fear_delta()
    state.add_fear()  # Already at max — should not change delta
    assert state._last_fear_delta == 0

def test_fear_at_min_does_not_set_delta():
    state = GameState()
    state.subtract_fear()  # Already at min — should not change delta
    assert state._last_fear_delta == 0


# ── Hope ──────────────────────────────────────────────────────────────────────

def test_hope_starts_at_zero():
    assert GameState().hope == 0

def test_hope_increments():
    state = GameState()
    state.add_hope()
    assert state.hope == 1

def test_hope_decrements():
    state = GameState()
    state.add_hope()
    state.add_hope()
    state.subtract_hope()
    assert state.hope == 1

def test_hope_does_not_exceed_max():
    state = GameState()
    for _ in range(20):
        state.add_hope()
    assert state.hope == 12  # HOPE_MAX

def test_hope_does_not_go_below_min():
    state = GameState()
    state.subtract_hope()
    assert state.hope == 0  # HOPE_MIN

def test_hope_add_sets_positive_delta():
    state = GameState()
    state.add_hope()
    assert state._last_hope_delta == +1

def test_hope_subtract_sets_negative_delta():
    state = GameState()
    state.add_hope()
    state.consume_hope_delta()
    state.subtract_hope()
    assert state._last_hope_delta == -1


# ── Delta consumption ─────────────────────────────────────────────────────────

def test_fear_delta_consumed_after_read():
    state = GameState()
    state.add_fear()
    assert state.consume_fear_delta() == +1
    assert state.consume_fear_delta() == 0  # Consumed — should be zero now

def test_hope_delta_consumed_after_read():
    state = GameState()
    state.add_hope()
    assert state.consume_hope_delta() == +1
    assert state.consume_hope_delta() == 0

def test_fear_changed_true_after_add():
    state = GameState()
    state.add_fear()
    assert state.fear_changed is True

def test_fear_changed_false_after_consume():
    state = GameState()
    state.add_fear()
    state.consume_fear_delta()
    assert state.fear_changed is False

def test_hope_changed_true_after_add():
    state = GameState()
    state.add_hope()
    assert state.hope_changed is True

def test_hope_changed_false_after_consume():
    state = GameState()
    state.add_hope()
    state.consume_hope_delta()
    assert state.hope_changed is False


# ── Reset ─────────────────────────────────────────────────────────────────────

def test_reset_clears_fear():
    state = GameState()
    state.add_fear()
    state.reset()
    assert state.fear == 0

def test_reset_clears_hope():
    state = GameState()
    state.add_hope()
    state.reset()
    assert state.hope == 0

def test_reset_clears_all():
    state = GameState()
    state.add_fear()
    state.add_hope()
    state.reset()
    assert state.fear == 0
    assert state.hope == 0

def test_reset_clears_fear_delta():
    state = GameState()
    state.add_fear()
    state.reset()
    assert state.consume_fear_delta() == 0

def test_reset_clears_hope_delta():
    state = GameState()
    state.add_hope()
    state.reset()
    assert state.consume_hope_delta() == 0


# ── Independence ──────────────────────────────────────────────────────────────

def test_fear_and_hope_are_independent():
    state = GameState()
    for _ in range(5):
        state.add_fear()
    for _ in range(3):
        state.add_hope()
    assert state.fear == 5
    assert state.hope == 3

def test_fear_delta_does_not_affect_hope_delta():
    state = GameState()
    state.add_fear()
    assert state.consume_hope_delta() == 0
