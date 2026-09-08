#player movement and collision detection
import pygame as pg
import settings as st
import math

class Player:
    def __init__(self):
        self.x , self.y = st.PLAYER_POS # x = 5.0 , y = 3.0
        self.angle = st.PLAYER_ANGLE # angle = 4.71239
        self.speed = st.PLAYER_SPEED # speed = 2 world units per second
        self.rotation_speed = st.PLAYER_ROTATION_SPEED # rotation speed in radians per second

    def get_direction(self):
        #calculate the direction vector based on the player's angle
        dir_x = math.cos(self.angle)
        dir_y = math.sin(self.angle)

        return dir_x , dir_y
    
    def update(self, dt: float):
        # Update the player's state based on input and elapsed time.
        keys = pg.key.get_pressed()
        delta_angle = 0.0
        if keys[pg.K_a]:  # Turn left
            delta_angle -= self.rotation_speed * dt
        if keys[pg.K_d]:  # Turn right
            delta_angle += self.rotation_speed * dt
        self.angle += delta_angle
        self.angle %= 2 * math.pi  # Keep the orientation within one revolution to maintain a predictable state.

        dir_x, dir_y = self.get_direction()
        #accumulated movement
        dx, dy = 0.0, 0.0
        #movment of this frame
        move_x = dir_x * self.speed * dt  
        move_y = dir_y * self.speed * dt

        if keys[pg.K_w]:  # Move forward
            dx += move_x
            dy += move_y
        if keys[pg.K_s]: # Move backward
            dx -= move_x
            dy -= move_y

        self.x += dx
        self.y += dy
        

#checking for player direction
#p1 = Player()
#dir_x , dir_y = p1.get_direction()
#print(f"Player direction: ({dir_x:.2f}, {dir_y:.2f})")
      