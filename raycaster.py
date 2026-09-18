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

        # calculate delta t_x and delta t_y for stepping to the next grid cell
        if dx != 0:
            delta_t_x = 1/abs(dx)
        else:
            delta_t_x = float("inf")  # No movement in x direction
        if dy != 0:
            delta_t_y = 1/abs(dy)
        else:
            delta_t_y = float("inf")  # No movement in y direction

        # Perform the DDA algorithm to find the wall hit
        hit_t = None  # Initialize hit_t to None
        while True:
            if t_x < t_y:
                grid_x+= step_x
                if (
                    grid_y < 0
                    or grid_y >= len(self.maze.grid)
                    or grid_x < 0
                    or grid_x >= len(self.maze.grid[grid_y])
                ):
                    break

                if self.maze.grid[grid_y][grid_x] == 1:
                    hit_t = t_x
                    break
                t_x += delta_t_x
            else:
                grid_y+= step_y
                if (
                    grid_y < 0
                    or grid_y >= len(self.maze.grid)
                    or grid_x < 0
                    or grid_x >= len(self.maze.grid[grid_y])
                ):
                    break

                if self.maze.grid[grid_y][grid_x] == 1:
                    hit_t = t_y
                    break
                t_y += delta_t_y

        return hit_t