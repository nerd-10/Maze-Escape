#main game class

import pygame as pg
import settings as st

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        pg.display.set_caption(st.WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.running = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    def update(self):
        self.dt = self.clock.tick(st.FPS) / 1000
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()