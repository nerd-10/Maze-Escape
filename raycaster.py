# Core rendering algorithm
# Cast ONE ray from the player and find the wall it hits

#import pygame as pg
from player import Player
from maze import Maze
#import settings as st

class Raycaster:
    def __init__(self, player: Player, maze: Maze):
        self.player = player
        self.maze = maze

    def cast_ray(self, x: float, y: float, dx: float, dy: float):
        # converting player world position to grid coordinates
        grid_x, grid_y = self.maze.world_to_grid(x, y)

        # Determine step_x and step_y from dx and dy 1, -1, or 0
        step_x = 1 if dx > 0 else -1 if dx < 0 else 0
        step_y = 1 if dy > 0 else -1 if dy < 0 else 0

        # Calculate the first X and Y boundary distances.
        if step_x != 0:
            if step_x > 0:
                next_x_boundary = grid_x + 1
            else:
                next_x_boundary = grid_x
        if step_y != 0:
            if step_y > 0:
                next_y_boundary = grid_y + 1
            else:
                next_y_boundary = grid_y

        # Calculate the distance to the next X and Y boundaries.
        if step_x != 0:
            t_x = (next_x_boundary - x) / dx
        else:
            t_x = float("inf")  # No movement in x direction

        if step_y != 0:
            t_y = (next_y_boundary - y) / dy
        else:
            t_y = float("inf")  # No movement in y direction
