#main game class
import pygame as pg
import settings as st
from player import Player
from maze import Maze

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        self.maze = Maze()
        pg.display.set_caption(st.WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.running = True
        self.player = Player(self.maze)  # Create a player instance 

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False


    def update(self, dt: float):
        # Update game state here
        self.player.update(dt)  # Update the player with the elapsed time

    def render(self):
        self.screen.fill(st.BACKGROUND_COLOR)  # Clear the screen
        for y, row in enumerate(self.maze.grid):
            for x,cell in enumerate(row):
                if cell ==1: # wall
                    wall_rect = pg.Rect(x * st.WORLD_SCALE, y * st.WORLD_SCALE, st.WORLD_SCALE, st.WORLD_SCALE)
                    pg.draw.rect(self.screen, st.DEBUG_WALL_COLOR, wall_rect) # draw the wall as a rectangle

        player_pos = (self.player.x * st.WORLD_SCALE, self.player.y * st.WORLD_SCALE) #player postion to screen postion
        pg.draw.circle(self.screen, st.DEBUG_PLAYER_COLOR, player_pos, st.DEBUG_PLAYER_RADIUS)  # Draw the player as a circle
        player_direction = self.player.get_direction()
        line_end = (
            player_pos[0] + player_direction[0] * st.DEBUG_DIRECTION_LENGTH * st.WORLD_SCALE, 
            player_pos[1] + player_direction[1] * st.DEBUG_DIRECTION_LENGTH * st.WORLD_SCALE
        ) #calculating a direction-line endpoint using a fixed debug length.
        pg.draw.line(self.screen, st.DEBUG_DIRECTION_COLOR, player_pos, line_end, 2)  # drawing a line from the player to that endpoint
        # Render game objects here
        pg.display.flip()  # Update the display

    def run(self):
        while self.running:

            self.handle_events()
            self.dt = self.clock.tick(st.FPS) / 1000
            self.update(self.dt)
            self.render()


'''
if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()  
'''