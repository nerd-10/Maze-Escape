#constants and configuration

WINDOW_TITLE = "Maze Escape"
RES = WIDTH , HEIGHT = 1200 , 600
HALF_WIDTH , HALF_HEIGHT = WIDTH // 2 , HEIGHT // 2
FPS = 60
BACKGROUND_COLOR = (100, 100, 100)  # RGB color for background
WORLD_SCALE = 64 #size of a single world unit in pixels
DEBUG_PLAYER_RADIUS = 10
DEBUG_DIRECTION_LENGTH = 1.0

#player settings

PLAYER_POS = 5.0, 3.0 #x ,y
PLAYER_ANGLE = 4.71239 #angle in radians 3 * math.pi / 2, 270°
PLAYER_SPEED = 2 #movement speed 2 world units per second
PLAYER_ROTATION_SPEED = 2 #rotation speed in radians per second