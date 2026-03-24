# Daggerheart Fear Tracker

A hardware-independent Fear/Hope tracker for the Daggerheart tabletop RPG system. Built with Python and Pygame, designed to run on a laptop during development and deploy to a Raspberry Pi with a small display and physical buttons.

## Design Philosophy

Three core principles guide every decision:

- **Hardware-agnostic core** — game logic and animation logic contain zero hardware references
- **Config-driven layout** — all dimensions, colors, and input mappings live in `config.py`
- **Keyboard-first development** — the app runs fully on a laptop so development and testing happen before any hardware exists

## Project Structure

```text
daggerheart_tracker/
├── main.py                  # Entry point — initialises Pygame, wires everything together
├── config.py                # ALL display dimensions, colors, input mappings, game rules
├── core/
│   ├── game_state.py        # Fear/Hope values, rules, min/max limits
│   └── input_handler.py     # Translates button presses into game actions
├── display/
│   ├── renderer.py          # Draws the full scene each frame
│   ├── gem_animator.py      # Sprite sheet loading, frame stepping, animation state
│   └── layout.py            # Computes screen regions from config values
├── assets/
│   ├── sprites/
│   │   ├── fear_gem.png     # Fear gem sprite sheet (all animation frames in one PNG)
│   │   └── hope_gem.png     # Hope gem sprite sheet
│   └── fonts/
│       └── pixel_font.ttf   # Pixel-style font for the counter display
└── tests/
    ├── test_game_state.py   # Unit tests for game logic (no Pygame required)
    └── test_input.py        # Unit tests for input translation
```

## Screen Layout

```text
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   F E A R                         H O P E              │
│                                                         │
│      7    ◄────── counter ────────►    4                │
│                                                         │
│  ◆ ◆ ◆ ◆ ◆ ◆         ◆ ◆ ◆ ◆                          │
│  ◆ ◇ ◇ ◇ ◇ ◇         ◇ ◇ ◇ ◇ ◇ ◇                      │
│  ↑ filled  ↑ empty   ↑ filled  ↑ empty                 │
│                                                         │
│          ↑ / ↓ Fear        → / ← Hope                  │
│                        [R] Reset                        │
└─────────────────────────────────────────────────────────┘

◆ = filled gem (animated on change)
◇ = empty gem slot (static, dimmed)
```

The display is split into two vertical halves — Fear (left, gold) and Hope (right, teal). Each half shows a label, a large numeric counter, and a 2-row grid of up to 12 gems.

## Requirements

- Python 3.10+
- pygame
- RPi.GPIO *(optional — Raspberry Pi hardware only)*

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
python main.py
```

### Keyboard Controls (Development)

| Key | Action |
| --- | --- |
| `↑` | Add Fear |
| `↓` | Subtract Fear |
| `→` | Add Hope |
| `←` | Subtract Hope |
| `R` | Reset both to 0 |
| `Q` | Quit |

## Configuration

All configuration lives in `config.py`. This is the **only file that changes** when swapping hardware.

Key settings:

```python
SCREEN_WIDTH  = 480     # Match to your display
SCREEN_HEIGHT = 320
FULLSCREEN    = False   # Set True on Pi

GEM_SCALE     = 3       # Pixel art scale multiplier

FEAR_MAX      = 12      # Daggerheart standard
HOPE_MAX      = 12

USE_GPIO      = False   # Set True on Raspberry Pi
```

## Running Tests

The core game logic has no Pygame or GPIO dependencies and can be unit tested on any machine:

```bash
python -m pytest tests/
```

## Sprite Sheet Specifications

| Property | Specification |
| --- | --- |
| Native frame size | 32×32 pixels per frame |
| Sheet layout | Frames left-to-right in a single row |
| Frame count | 8 frames per animation |
| Sheet dimensions | 256×32 pixels |
| File format | PNG with transparency (RGBA) |
| Scaling method | Nearest-neighbor (preserves pixel art look) |

The vanish animation is the appear animation played in reverse — no separate asset needed.

## Build Order

| Step | What to Build | How to Test |
| --- | --- | --- |
| 1 | `config.py` | Python import — no errors |
| 2 | `game_state.py` | Unit tests — no Pygame needed |
| 3 | `main.py` skeleton | See a black Pygame window |
| 4 | `input_handler.py` (keyboard) | Print actions to terminal each frame |
| 5 | `layout.py` | Print computed coordinates |
| 6 | `renderer.py` (labels and counters only) | See FEAR/HOPE labels and 0/0 on screen |
| 7 | Wire input → game_state → renderer | Press keys, see counters change |
| 8 | `gem_animator.py` (static gems first) | See gem grid update on key press |
| 9 | Add sprite animation | See gem appear/vanish on add/subtract |
| 10 | GPIO input layer | Set `USE_GPIO=True`, test with buttons |
| 11 | Autostart systemd service on Pi | Power cycle Pi, app starts automatically |

Steps 1–9 happen entirely on a laptop. Step 10 is the only step that requires hardware.

## Hardware Deployment (Raspberry Pi)

1. Set `USE_GPIO = True` in `config.py`
2. Set `FULLSCREEN = True` and update `SCREEN_WIDTH`/`SCREEN_HEIGHT` to match your display
3. Uncomment `RPi.GPIO` in `requirements.txt` and run `pip install -r requirements.txt`
4. Map GPIO pins in `config.py` to match your wiring:

```python
GPIO_FEAR_ADD      = 17   # D-pad Up
GPIO_FEAR_SUBTRACT = 27   # D-pad Down
GPIO_HOPE_ADD      = 22   # D-pad Right
GPIO_HOPE_SUBTRACT = 23   # D-pad Left
GPIO_RESET         = 24   # A button
GPIO_QUIT          = 25   # B button
```
