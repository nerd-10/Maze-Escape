#maze generating algorithm
#"Given a world position, which maze cell contains it?

def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
    # convert world coordinates into grid coordinates
    grid_x = int(x)
    grid_y = int(y)

    return grid_x, grid_y