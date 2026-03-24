# ── Display ──────────────────────────────────────────────────────────────────
SCREEN_WIDTH      = 800    # Change to match final display (e.g. 800)
SCREEN_HEIGHT     = 480    # Change to match final display (e.g. 480)
SCREEN_MIN_WIDTH  = 400
SCREEN_MIN_HEIGHT = 240
FPS           = 30     # Frames per second — 30 is smooth, 60 unnecessary
FULLSCREEN    = False  # Set True on Pi; False during laptop development
RESIZABLE     = True   # Allow window resizing during laptop development; set False on Pi

# ── Sprite scaling ────────────────────────────────────────────────────────────
GEM_NATIVE_SIZE  = 32                          # Native pixel art size (32x32 per frame)
GEM_SCALE        = 3                           # Scale multiplier — nearest-neighbor (keeps pixel look)
GEM_DISPLAY_SIZE = GEM_NATIVE_SIZE * GEM_SCALE # = 96px rendered size
GEM_COLS_MAX     = 6                           # Starting columns; wraps in steps of 2 as window shrinks

# ── Game rules ────────────────────────────────────────────────────────────────
FEAR_MIN = 0
FEAR_MAX = 12  # Daggerheart standard maximum
HOPE_MIN = 0
HOPE_MAX = 6  # Daggerheart standard maximum

# ── Animation ─────────────────────────────────────────────────────────────────
ANIM_APPEAR_FRAMES  = 8   # Number of frames in the 'gem appears' animation
ANIM_VANISH_FRAMES  = 8   # Number of frames in the 'gem vanishes' animation
ANIM_FRAME_DURATION = 60  # Milliseconds per frame (60ms = ~16fps for animation)

# ── Colors (RGB tuples) ───────────────────────────────────────────────────────
COLOR_BG        = ( 18,  10,  30)  # Near-black background
COLOR_FEAR_TEXT = ( 46, 139, 122)  # Teal for fear label and counter
COLOR_HOPE_TEXT = (201, 168,  76)  # Gold for hope label and counter
COLOR_UI_MUTED  = (122, 107, 138)  # Muted purple for hint text

# ── Input: Keyboard (development / laptop) ────────────────────────────────────
KEY_FEAR_ADD      = 'up'
KEY_FEAR_SUBTRACT = 'down'
KEY_HOPE_ADD      = 'right'
KEY_HOPE_SUBTRACT = 'left'
KEY_RESET         = 'r'
KEY_QUIT          = 'q'

# ── Input: GPIO (Raspberry Pi hardware) ───────────────────────────────────────
# Set USE_GPIO = True when running on Pi hardware
USE_GPIO           = False
GPIO_FEAR_ADD      = 17  # D-pad Up
GPIO_FEAR_SUBTRACT = 27  # D-pad Down
GPIO_HOPE_ADD      = 22  # D-pad Right
GPIO_HOPE_SUBTRACT = 23  # D-pad Left
GPIO_RESET         = 24  # A button
GPIO_QUIT          = 25  # B button (long-press to quit)
