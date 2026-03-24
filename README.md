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
│   └── layout.py            # Computes screen regions dynamically from window size
├── assets/
│   ├── sprites/
│   │   ├── fear_gem.png     # Fear gem sprite sheet (all animation frames in one PNG)
│   │   └── hope_gem.png     # Hope gem sprite sheet
│   └── fonts/
│       └── pixel_font.ttf   # Pixel-style font for the counter display (optional)
├── .vscode/
│   └── launch.json          # VSCode Run and Debug configurations
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
│            ↑/↓ Fear   →/← Hope   [R] Reset             │
│                          [Q] Quit                       │
└─────────────────────────────────────────────────────────┘

◆ = filled gem (animated on change)
◇ = empty gem slot (static, dimmed)
```

The display is split into two vertical halves — Fear (left, gold) and Hope (right, teal). Each half shows a label, a large numeric counter, and a 2-row grid of up to 12 gems. The layout recalculates automatically when the window is resized.

---

## Setup

### 1. Prerequisites

- Python 3.10 or later — [python.org](https://www.python.org/downloads/)
- VSCode with the **Python** extension installed

### 2. Create a virtual environment

Open the project folder in VSCode, then open the integrated terminal (`Ctrl+`` `).

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> **Windows Defender note:** If you see a `Permission denied` error on `.venv\Scripts\python.exe`,
> add the project folder to Windows Defender's exclusion list:
> **Windows Security → Virus & threat protection → Exclusions → Add folder**
> then re-run the commands above.

### 3. Select the interpreter in VSCode

1. Press `Ctrl+Shift+P` and type `Python: Select Interpreter`
2. Choose the entry showing `.venv`:
   `Python 3.x.x ('.venv': venv) .\.venv\Scripts\python.exe`

The status bar at the bottom of VSCode will update to show the active interpreter.

---

## Running the App

### Via Run and Debug (recommended)

1. Press `Ctrl+Shift+D` to open the Run and Debug panel
2. Select a configuration from the dropdown:
   - **Run Daggerheart Tracker** — launches `main.py`
   - **Run Tests** — runs `pytest` across the `tests/` folder
3. Press `F5` to start

### Via terminal

```bash
python main.py
```

---

## Keyboard Controls

| Key | Action |
| --- | --- |
| `↑` | Add Fear |
| `↓` | Subtract Fear |
| `→` | Add Hope |
| `←` | Subtract Hope |
| `R` | Reset both to 0 |
| `Q` | Quit |

---

## Configuration

All configuration lives in `config.py`. This is the **only file that changes** when swapping hardware.

Key settings:

```python
SCREEN_WIDTH  = 480     # Starting window width (resizable during development)
SCREEN_HEIGHT = 320     # Starting window height
FULLSCREEN    = False   # Set True on Pi
RESIZABLE     = True    # Allow window resizing on laptop; set False on Pi

GEM_SCALE     = 3       # Pixel art scale multiplier (gem size auto-fits the window)

FEAR_MAX      = 12      # Daggerheart standard
HOPE_MAX      = 12

USE_GPIO      = False   # Set True on Raspberry Pi
```

> **Window resizing:** The layout recalculates whenever the window is resized, so gem grids,
> counters, and labels always scale and reposition correctly. No manual size changes needed.

---

## Running Tests

The core game logic has no Pygame or GPIO dependencies and can be unit tested on any machine:

```bash
python -m pytest tests/
```

---

## Sprite Sheet Specifications

Sprite assets are optional during development — the renderer draws fallback gem shapes automatically when no PNG files are found in `assets/sprites/`.

| Property | Specification |
| --- | --- |
| Native frame size | 32×32 pixels per frame |
| Sheet layout | Frames left-to-right in a single row |
| Frame count | 8 frames per animation |
| Sheet dimensions | 256×32 pixels |
| File format | PNG with transparency (RGBA) |
| Scaling method | Nearest-neighbor (preserves pixel art look) |

The vanish animation is the appear animation played in reverse — no separate asset needed.

---

## Hardware Deployment (Raspberry Pi)

1. Set `USE_GPIO = True` and `RESIZABLE = False` and `FULLSCREEN = True` in `config.py`
2. Update `SCREEN_WIDTH` / `SCREEN_HEIGHT` to match your display resolution
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

Steps 1–9 of the build order happen entirely on a laptop. Step 10 is the only step that requires hardware.
