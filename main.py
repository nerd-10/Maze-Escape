# Entry point
import pygame as pg
import settings as s
    
pg.init()
screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption(s.WINDOW_TITLE)
running = True
dt = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(s.FPS) / 1000  # Limit to FPS and get delta time in seconds
    fps = clock.get_fps()
    pg.display.set_caption(f"{s.WINDOW_CAPTION} - FPS: {fps:.2f}")
    pg.display.flip()
   
pg.quit()