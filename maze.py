# maze generating algorithm
# Given a world position, which maze cell contains it?
import math as mt
import random


class Maze:
    def __init__(self):
        self.generate_new_maze()

    def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        grid_x = int(x)
        grid_y = int(y)

        return grid_x, grid_y

    def is_walkable(self, x: float, y: float) -> bool:
        grid_x, grid_y = self.world_to_grid(x, y)
        if grid_y < 0 or grid_y >= len(self.grid):
            return False
        if (
            grid_x < 0 or grid_x >= len(self.grid[grid_y])
        ):  # because self.grid[grid_y] is one row, and its length is the number of columns.
            return False

        return (
            self.grid[grid_y][grid_x] == 0
        )  # because rows correspond to Y and columns correspond to X.

    def is_gateway(self, x: float, y: float) -> bool:
        gateway_position_x, gateway_position_y = self.gateway_pos
        dx = x - gateway_position_x
        dy = y - gateway_position_y
        dx_squared = dx**2
        dy_squared = dy**2
        distance_squared = dx_squared + dy_squared
        distance = mt.sqrt(distance_squared)
        active = False
        gateway_activation_radius = 0.5
        if distance <= gateway_activation_radius:
            active = True
        return active

    def generate_new_maze(self):
        rows = 11
        cols = 15
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        start_x = 1
        start_y = 1
        directions = [
            (0, -2),  # up
            (0, 2),  # down
            (-2, 0),  # left
            (2, 0),  # right
        ]
        stack = []
        while True:
            valid_directions = []
            for dx, dy in directions:
                candidate_x = start_x + dx
                candidate_y = start_y + dy

                # check candidate is inside the maze and not on the outer boundary.
                if (
                    1 <= candidate_x < cols - 1
                    and 1 <= candidate_y < rows - 1
                    and self.grid[candidate_y][candidate_x] == 1
                ):
                    valid_directions.append((dx, dy))

            if not valid_directions:
                if stack:
                    start_x, start_y = stack.pop()
                    continue
                else:
                    break
            dx, dy = random.choice(valid_directions)
            stack.append((start_x, start_y))
            candidate_x = start_x + dx
            candidate_y = start_y + dy
            wall_x = start_x + (dx // 2)
            wall_y = start_y + (dy // 2)
            self.grid[start_y][start_x] = 0
            self.grid[wall_y][wall_x] = 0
            self.grid[candidate_y][candidate_x] = 0
            start_x = candidate_x
            start_y = candidate_y

        gateway_candidates = []
        for y in range(1, rows - 1):
            for x in range( 1, cols - 1):
                if self.grid[y][x] == 0:
                    gateway_candidates.append((x, y))

        farthest_cell = None
        farthest_distance = -1
        for x, y in gateway_candidates:
            dx = x - 1
            dy = y - 1
            distance = mt.sqrt(dx**2 + dy**2)
            if distance > farthest_distance:
                farthest_distance = distance
                farthest_cell = (x, y)
        gateway_x, gateway_y = farthest_cell
        self.gateway_pos = (farthest_cell[0] + 0.5, farthest_cell[1] + 0.5)  # center of the cell
        self.player_start_pos = 1.5, 1.5

