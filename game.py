# main game class
import pygame as pg

import settings as st
from animation import Animation
from gateway import Gateway
from maze import Maze
from player import Player
from raycaster import Raycaster
from renderer import Renderer
from texture import TextureManager


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        self.texture_manager = TextureManager(
            "assets/floor/floor.png", 
            "assets/wall_textures"
            )
        self.texture_manager.load_texture()
        self.maze = Maze()
        pg.display.set_caption(st.WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.running = True
        self.player = Player(
            self.maze
        ) 
        self.raycaster = Raycaster(self.player, self.maze)
        self.gateway =  Gateway("assets/door/door.png")
        self.gateway_animation = Animation(self.gateway.frames)
        self.renderer = Renderer(self.screen, self.player, self.raycaster, self.maze, self.gateway, self.gateway_animation)
        self.maze_completed = False
        self.elapsed_time = 0.0
        self.completion_time = None

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self, dt: float):
        self.gateway_animation.update(dt)
        gateway_reached = self.player.update(
            dt
        )  # Update the player with the elapsed time
        if not self.maze_completed:
            self.elapsed_time += dt
        if gateway_reached and not self.maze_completed:
            print("Gateway Reached!")
            self.completion_time = self.elapsed_time
            print(f"completion time : {self.completion_time:.2f}")
            self.maze_completed = True
            self.maze.generate_new_maze()
            self.reset_maze_run()
            self.player.reset_player_position()  # Reset player position after maze completion

    def reset_maze_run(self):
        self.elapsed_time = 0.0
        self.maze_completed = False

    def render(self):
        self.screen.fill(st.BACKGROUND_COLOR)  
        self.renderer.render()
        self.screen.blit(
            pg.font.Font(None, 24).render(
                f"FPS: {self.clock.get_fps():.1f}", True, "white"
            ),
            (10, 10),
        )
        self.screen.blit(
            pg.font.Font(None, 24).render(
                f"Elapsed Time: {self.elapsed_time:.2f}", True, "yellow"
            ),
            (10,40)
        )
        pg.display.flip()  # Update the display

    def run(self):
        while self.running:
            self.handle_events()
            self.dt = self.clock.tick(st.FPS) / 1000
            self.update(self.dt)
            self.render()
