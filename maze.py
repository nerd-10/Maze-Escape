# maze generating algorithm
# Given a world position, which maze cell contains it?
import math as mt


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
            (0,-2) #up,
            (0, 2) # down,
            (-2, 0) #left,
            (2, 0) #right
        ]
        
        self.grid[start_y][start_x] = 0
        print(self.grid[1][1])
        self.gateway_pos = (11.5, 9.5)
        self.player_start_pos = 3.5, 3.5

c = Maze()
print(c)