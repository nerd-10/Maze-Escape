# Screen drawing
import math as mt

import pygame as pg

import settings as st


class Renderer:
    def __init__(self, screen, player, raycaster, maze):
        self.screen = screen
        self.player = player
        self.raycaster = raycaster
        self.maze = maze

    def render_walls(self):
        # CEILING
        pg.draw.rect(
            self.screen, st.CEILING_COLOR, (0, 0, st.WIDTH, st.HEIGHT // 2)
            )
        # FLOOR
        pg.draw.rect(
            self.screen, st.FLOOR_COLOR, (0, st.HEIGHT // 2, st.WIDTH, st.HEIGHT // 2)
        )

        fwd_x, fwd_y = self.player.get_direction()
        right_vector_x = -(fwd_y)
        right_vector_y = fwd_x
        horizon = st.HEIGHT / 2
        camera_height = 0.5
        focal_length = (st.HEIGHT / 2) / (mt.tan(st.FOV / 2))

        for test_row in range(int(horizon) + 1, st.HEIGHT, 4):
            vertical_depth = test_row - horizon
            depth = (camera_height * focal_length) / vertical_depth
            for test_column in range(0, st.WIDTH, 4):
                horizonatal_direction = test_column / (st.WIDTH - 1)
                c = 2 * horizonatal_direction - 1
                plane_x = c * (mt.tan(st.FOV / 2)) * right_vector_x
                plane_y = c * (mt.tan(st.FOV / 2)) * right_vector_y
                dx = fwd_x + plane_x
                dy = fwd_y + plane_y
                world_x = self.player.x + depth * dx
                # world_y = self.player.y + depth * dy
                fraction_x = world_x - mt.floor(world_x)
                shade_x = int(fraction_x * 255)
                shade_tuple = (shade_x, shade_x, shade_x)
                pg.draw.rect(self.screen, shade_tuple, (test_column, test_row, 4, 4))
        # rendering loop
        for screen_x in range(st.WIDTH):
            u = screen_x / (st.WIDTH - 1)
            ray_angle = self.player.angle + (u - 0.5) * st.FOV
            ray_dx = mt.cos(ray_angle)
            ray_dy = mt.sin(ray_angle)
            hit_t, hit_x, hit_y, hit_side, wall_pos = self.raycaster.cast_ray(  # noqa: RUF059
                self.player.x, self.player.y, ray_dx, ray_dy
            )
            if hit_t is None:
                continue
            cos_theta = fwd_x * ray_dx + fwd_y * ray_dy
            camera_depth = hit_t * cos_theta
            projection_height = (
                (st.WALL_HEIGHT)
                * (st.HEIGHT / 2)
                / ((camera_depth) * mt.tan(st.FOV / 2))
            )
            screen_center_y = st.HEIGHT / 2
            top = screen_center_y - (projection_height / 2)
            # bottom = screen_center_y + (projection_height/2)
            pg.draw.rect(
                self.screen,
                st.DEBUG_DIRECTION_COLOR,
                (screen_x, top, 1, projection_height),
            )
        gateway_x, gateway_y = self.maze.gateway_pos
        player_x = self.player.x
        player_y = self.player.y
        relative_x = gateway_x - player_x
        relative_y = gateway_y - player_y
        camera_x = relative_x * right_vector_x + relative_y * right_vector_y
        camera_depth = relative_x * fwd_x + relative_y * fwd_y
        if camera_depth <= 0:
            print("Gateway is behind the player.")
        else:
           screen_x = (
               (camera_x / camera_depth) * focal_length + (st.WIDTH / 2)
           )
           print(f"Screen X position: {screen_x}")
        gateway_angle = mt.atan2(camera_x, camera_depth)
        print(f"camera_x: {camera_x}, camera_depth: {camera_depth}")
        print(f"Player position: ({player_x}, {player_y})")
        print(f"Gateway position: ({gateway_x}, {gateway_y})")
        print(f"Relative position: ({relative_x}, {relative_y})")
        print(f"Camera coordinates: ({camera_x}, {camera_depth})")
        print(f"Gateway angle: {gateway_angle}")
        
