#maze generating algorithm
#"Given a world position, which maze cell contains it?

class Maze:
    def __init__(self):
        self.grid =[   #1 is wall and 0 is path
            [1,1,1,1,1], 
            [1,1,0,0,1],
            [1,0,0,0,1],
            [1,1,1,0,1],
            [1,1,1,1,1]
        ]
    
    def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        grid_x = int(x)
        grid_y = int(y)

        return grid_x, grid_y

    def is_walkable(self, x: float, y: float) -> bool:
        grid_x, grid_y = self.world_to_grid(x, y)
        if grid_y < 0 or grid_y >=len(self.grid):
            return False
        if grid_x < 0 or grid_x >=len(self.grid[grid_y]): #because self.grid[grid_y] is one row, and its length is the number of columns.
            return False
        
        return self.grid[grid_y][grid_x] == 0 #because rows correspond to Y and columns correspond to X.