# constants and configuration

WINDOW_TITLE = "Maze Escape"
RES = WIDTH, HEIGHT = 1200, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
BACKGROUND_COLOR = (100, 100, 100)  # RGB color for background
WORLD_SCALE = 64  # size of a single world unit in pixels
FOV = 1.0472  # 60° in radians
WALL_HEIGHT = 1.0  # height of the wall in world units
CEILING_COLOR = (1, 1, 1)
FLOOR_COLOR = (0, 255, 255)
GATEWAY_HEIGHT = 1.0  # height of the gateway in world units

# debug settings

DEBUG_PLAYER_RADIUS = 10
DEBUG_DIRECTION_LENGTH = 1.0
DEBUG_WALL_COLOR = (0, 0, 0)
DEBUG_PLAYER_COLOR = (255, 255, 255)
DEBUG_DIRECTION_COLOR = (255, 0, 0)

# player settings

PLAYER_SPEED = 2  # movement speed 2 world units per second
PLAYER_ROTATION_SPEED = 2  # rotation speed in radians per second
