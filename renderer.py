# Screen drawing
import pygame as pg
import settings as st
import math as mt

class Renderer:
    def __init__(self, screen, player, raycaster):
        self.screen = screen
        self.player = player
        self.raycaster = raycaster

    def render_walls(self):
        fwd_x, fwd_y = self.player.get_direction()
        
        #CEILING
        pg.draw.rect(self.screen, st.CEILING_COLOR,(0, 0, st.WIDTH, st.HEIGHT//2))
        #FLOOR
        pg.draw.rect(self.screen, st.FLOOR_COLOR,(0, st.HEIGHT//2, st.WIDTH ,st.HEIGHT//2))
        for screen_x in range(st.WIDTH):
            u = screen_x / (st.WIDTH -1)
            ray_angle = (self.player.angle + (u - 0.5) * st.FOV)
            ray_dx = mt.cos(ray_angle)
            ray_dy = mt.sin(ray_angle)
            hit_t, hit_x, hit_y, hit_side, wall_pos = (
                self.raycaster.cast_ray(self.player.x,self.player.y, ray_dx,ray_dy)
                )
            if hit_t is None:
                continue
            cos_theta = (fwd_x * ray_dx + fwd_y * ray_dy)
            camera_depth = hit_t * cos_theta
            projection_height = ((st.WALL_HEIGHT) * (st.HEIGHT/2) / ((camera_depth) * mt.tan(st.FOV/2)))
            screen_center_y = st.HEIGHT/2
            top = screen_center_y - (projection_height/2)
            #bottom = screen_center_y + (projection_height/2)
            pg.draw.rect(self.screen, st.DEBUG_DIRECTION_COLOR,(screen_x, top, 1, projection_height))