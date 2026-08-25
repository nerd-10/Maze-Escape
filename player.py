#player movement and collision detection
#import pygame as pg
import settings as st
import math

class Player:
    def __init__(self):
        self.x , self.y = st.PLAYER_POS # x = 5.0 , y = 3.0
        self.angle = st.PLAYER_ANGLE # angle = 4.71239
        self.speed = st.PLAYER_SPEED # speed = 2 world units per second

    def get_direction(self):
        #calculate the direction vector based on the player's angle
        dir_x = math.cos(self.angle)
        dir_y = math.sin(self.angle)

        return dir_x , dir_y


#p1 = Player()
#dir_x , dir_y = p1.get_direction()
#print(f"Player direction: ({dir_x:.2f}, {dir_y:.2f})")
