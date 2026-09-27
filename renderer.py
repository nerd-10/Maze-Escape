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
        #CEILING
        pg.draw.rect(self.screen, st.CEILING_COLOR,(0, 0, st.WIDTH, st.HEIGHT//2))
        #FLOOR
        pg.draw.rect(self.screen, st.FLOOR_COLOR,(0, st.HEIGHT//2, st.WIDTH ,st.HEIGHT//2))

        fwd_x, fwd_y = self.player.get_direction()
        right_vector_x = -(fwd_y)
        right_vector_y = (fwd_x)
        horizon = st.HEIGHT/2
        camera_height = 0.5
        #test_row = 480
        #vertical_depth = test_row - horizon
        focal_length = (st.HEIGHT/2)/(mt.tan(st.FOV/2))
        #test_column = st.WIDTH//2
        #depth = (camera_height * focal_length)/vertical_depth

        for test_row in range(int(horizon) + 1, st.HEIGHT):
            vertical_depth = test_row - horizon
            depth = (camera_height * focal_length)/vertical_depth
            for test_column in range(st.WIDTH):
                horizonatal_direction = test_column/(st.WIDTH-1)
                c = 2*horizonatal_direction - 1
                plane_x = c*(mt.tan(st.FOV/2))*right_vector_x
                plane_y = c*(mt.tan(st.FOV/2))*right_vector_y
                dx = fwd_x + plane_x
                dy = fwd_y + plane_y
                world_x = self.player.x + depth * dx
                world_y = self.player.y + depth * dy

                if test_row == 480 and test_column == 0:
                    print("For 480 and 0")
                    print(f"Depth is: {depth}")
                    print(f"World coordinates are:" f"({world_x:.5f}, {world_y:.5f})")
                elif test_row == 480 and test_column == 1199:
                    print("For 480 and 1199")
                    print(f"Depth is: {depth}")
                    print(f"World coordinates are:" f"({world_x:.5f}, {world_y:.5f})")
                elif test_row == 600 and test_column == 0:
                    print("For 600 and 0")
                    print(f"Depth is: {depth}")
                    print(f"World coordinates are:" f"({world_x:.5f}, {world_y:.5f})")
                elif test_row == 600 and test_column == 1199:
                    print("For 600 and 1199")
                    print(f"Depth is: {depth}")
                    print(f"World coordinates are:" f"({world_x:.5f}, {world_y:.5f})")
        '''
        print(f"vertical depth is: {vertical_depth}")
        print(f"Horizon is: {horizon}")
        print(f"Depth is: {depth}")
        print(f"Focal Length is: {focal_length}")
        print(f"Horizontal Direction is : {horizonatal_direction}")
        print(f"c is : {c}")
        print(f"{fwd_x:.2f},{fwd_y:.2f}")
        print(f"Right vector is : {right_vector_x, right_vector_y}")
        print(f"Plane x is : {plane_x:.5f}")
        print(f"Plane y is : {plane_y:.5f}")
        print(f"Camera plane offset is : "f"({plane_x:.5f}, {plane_y:.5f})")
        print(f"Direction vector is : "f"({dx:.5f}, {dy:.5f})")
        print(f"World coordinates are:" f"({world_x:.5f}, {world_y:.5f})")
        '''

        #rendering loop
        for screen_x in range(st.WIDTH):
            u = screen_x / (st.WIDTH - 1)
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
