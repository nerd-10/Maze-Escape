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


    def update(self, dt: float):
        # Update game state here
        pass

    def render(self):
        self.screen.fill(st.BACKGROUND_COLOR)  # Clear the screen
        # Render game objects here
        pg.display.flip()  # Update the display

    def run(self):
        while self.running:

            self.handle_events()
            self.dt = self.clock.tick(st.FPS) / 1000
            self.update(self.dt)
            self.render()


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()  