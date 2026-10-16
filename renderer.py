    # Screen drawing
import math as mt

import pygame as pg

import settings as st


class Renderer:
    def __init__(self, screen, player, raycaster, maze, gateway, gateway_animation, texture_manager):
        self.screen = screen
        self.player = player
        self.raycaster = raycaster
        self.maze = maze
        self.gateway = gateway
        self.gateway_animation = gateway_animation
        self.texture_manager = texture_manager
        self.wall_depths = [float("inf")] * st.WIDTH

    def render(self):
        # CEILING
        pg.draw.rect(self.screen, st.CEILING_COLOR, (0, 0, st.WIDTH, st.HEIGHT // 2))
        # FLOOR
        pg.draw.rect(
            self.screen, st.FLOOR_COLOR, (0, st.HEIGHT // 2, st.WIDTH, st.HEIGHT // 2)
        )
        self.render_walls()
        self.render_floor()
        self.render_gateway()

    def get_camera_vectors(self):
        forward_x, forward_y = self.player.get_direction()
        right_x = -forward_y
        right_y = forward_x

        return forward_x, forward_y, right_x, right_y

    def project_world_point(self, world_x, world_y):
        forward_x, forward_y, right_vector_x, right_vector_y = self.get_camera_vectors()
        relative_x = world_x - self.player.x
        relative_y = world_y - self.player.y
        camera_x = relative_x * right_vector_x + relative_y * right_vector_y
        camera_depth = relative_x * forward_x + relative_y * forward_y

        return camera_x, camera_depth

    def project_to_screen(self, camera_x, camera_depth):
        focal_length = (st.HEIGHT / 2) / (mt.tan(st.FOV / 2))
        screen_x = (camera_x / camera_depth) * focal_length + (st.WIDTH / 2)

        return screen_x

    def is_point_visible(self, screen_x, gateway_depth):
        u = screen_x / (st.WIDTH - 1)
        ray_angle = self.player.angle + (u - 0.5) * st.FOV
        ray_dx = mt.cos(ray_angle)
        ray_dy = mt.sin(ray_angle)
        hit_t, *_ = self.raycaster.cast_ray(
            self.player.x, self.player.y, ray_dx, ray_dy
        )
        if hit_t is None:
            return True
        forward_x, forward_y, *_ = self.get_camera_vectors()
        cos_theta = forward_x * ray_dx + forward_y * ray_dy
        if cos_theta <= 0:
            return False

        wall_camera_depth = hit_t * cos_theta

        return gateway_depth < wall_camera_depth

    def clip_segment_near_plane(self, point_a, point_b, near_depth=0.05):
        x_a, depth_a = point_a
        x_b, depth_b = point_b

        if depth_a < near_depth and depth_b < near_depth:
            return None

        if depth_a < near_depth:
            t = (near_depth - depth_a) / (depth_b - depth_a)
            x_a = x_a + t * (x_b - x_a)
            depth_a = near_depth

        elif depth_b < near_depth:
            t = (near_depth - depth_b) / (depth_a - depth_b)
            x_b = x_b + t * (x_a - x_b)
            depth_b = near_depth

        return (x_a, depth_a), (x_b, depth_b)

    def render_walls(self):
        self.wall_depths = [float("inf")] * st.WIDTH
        fwd_x, fwd_y, right_vector_x, right_vector_y = self.get_camera_vectors()
        horizon = st.HEIGHT / 2
        camera_height = 0.5
        focal_length = (st.HEIGHT / 2) / (mt.tan(st.FOV / 2))

        for test_row in range(int(horizon) + 1, st.HEIGHT, 4):
            vertical_depth = test_row - horizon
            depth = (camera_height * focal_length) / vertical_depth
            for test_column in range(0, st.WIDTH, 4):
                horizontal_direction = test_column / (st.WIDTH - 1)
                c = 2 * horizontal_direction - 1
                plane_x = c * (mt.tan(st.FOV / 2)) * right_vector_x
                plane_y = c * (mt.tan(st.FOV / 2)) * right_vector_y
                dx = fwd_x + plane_x
                dy = fwd_y + plane_y
                ray_length = mt.sqrt(dx * dx + dy * dy)
                dx /= ray_length
                dy /= ray_length
                world_x = self.player.x + depth * dx
                world_y = self.player.y + depth * dy
                floor_texture = self.texture_manager.floor_texture
                texture_width = floor_texture.get_width()
                texture_height = floor_texture.get_height()
                texture_x = int(
                    (world_x - mt.floor(world_x)) * texture_width
                )
                texture_y = int(
                    (world_y - mt.floor(world_y)) * texture_height
                )
                texture_x = max(0, min(texture_x, texture_width - 1))
                texture_y = max(0, min(texture_y, texture_height - 1))
                floor_colour = floor_texture.get_at((texture_x, texture_y))

                pg.draw.rect(
                    self.screen,
                    floor_colour,
                    (test_column, test_row, 4, 4)
                )
        # rendering loop
        for screen_x in range(st.WIDTH):
            u = screen_x / (st.WIDTH - 1)
            ray_angle = self.player.angle + (u - 0.5) * st.FOV
            ray_dx = mt.cos(ray_angle)
            ray_dy = mt.sin(ray_angle)
            hit_t, hit_x, hit_y, hit_side, wall_pos = (
                self.raycaster.cast_ray(
                    self.player.x, self.player.y, ray_dx, ray_dy
                    )
                    )
            if hit_t is None:
                continue
            
            grid_x, grid_y = self.maze.world_to_grid(hit_x, hit_y)
            texture_index = self.maze.wall_texture_indices[grid_y][grid_x]
            texture = self.texture_manager.wall_textures[texture_index]
            texture_x = int(wall_pos * texture.get_width())
            texture_x = min(texture_x, texture.get_width() - 1)
            texture_column = texture.subsurface(
                (texture_x, 0, 1, texture.get_height())
            )
            cos_theta = fwd_x * ray_dx + fwd_y * ray_dy
            camera_depth = hit_t * cos_theta
            # Reject invalid or extremely close wall hits.
            if camera_depth <= 0.001:
                continue
            self.wall_depths[screen_x] = camera_depth
            projection_height = (
                st.WALL_HEIGHT * (st.HEIGHT / 2) / ((camera_depth) * mt.tan(st.FOV / 2))
            )
            screen_center_y = st.HEIGHT / 2
            top = screen_center_y - (projection_height / 2)
            bottom = screen_center_y + (projection_height / 2)

            # Clip the wall to the visible screen area.
            draw_top = max(0, int(top))
            draw_bottom = min(st.HEIGHT, int(bottom))

            if draw_bottom <= draw_top:
                continue
            scaled_column = pg.transform.scale(
                texture_column,
                (1, draw_bottom - draw_top)
                )
            self.screen.blit(
                scaled_column,
                (screen_x, draw_top)
                )

    def render_gateway(self):
        gateway_x, gateway_y = self.maze.gateway_pos
        gateway_orientation = self.maze.gateway_orientation
        render_x, render_y = gateway_x, gateway_y
        if gateway_orientation == "up":
            render_y = gateway_y + 0.5 - 0.01
        elif gateway_orientation == "down":
            render_y = gateway_y - 0.5 + 0.01
        elif gateway_orientation == "left":
            render_x = gateway_x + 0.5 - 0.01
        elif gateway_orientation == "right":
            render_x = gateway_x - 0.5 + 0.01
        half_width = 0.8 / 2
        if gateway_orientation in ("up", "down"):
            endpoint_a = (render_x - half_width, render_y)
            endpoint_b = (render_x + half_width, render_y)
        else:
            endpoint_a = (render_x, render_y - half_width)
            endpoint_b = (render_x, render_y + half_width)

        # Project the two endpoints into camera space.
        camera_x_a, camera_depth_a = self.project_world_point(*endpoint_a)
        camera_x_b, camera_depth_b = self.project_world_point(*endpoint_b)
        clipped_points = self.clip_segment_near_plane(
            (camera_x_a, camera_depth_a),
            (camera_x_b, camera_depth_b),
        )
        if clipped_points is None:
            return

        (camera_x_a, camera_depth_a), (camera_x_b, camera_depth_b) = clipped_points

        screen_x_a = self.project_to_screen(camera_x_a, camera_depth_a)
        screen_x_b = self.project_to_screen(camera_x_b, camera_depth_b)

        gateway_screen_width = abs(screen_x_b - screen_x_a)
        average_depth = (camera_depth_a + camera_depth_b) / 2
        gateway_screen_x = (screen_x_a + screen_x_b) / 2
        if average_depth > 0 and self.is_point_visible(gateway_screen_x, average_depth):
            gateway_screen_height = (
                st.GATEWAY_HEIGHT
                * (st.HEIGHT / 2)
                / (average_depth * mt.tan(st.FOV / 2))
            )
            screen_center_y = st.HEIGHT / 2
            top = screen_center_y - (gateway_screen_height / 2)
            left = min(screen_x_a, screen_x_b)
            gateway_frame = self.gateway_animation.get_current_frame()
            max_sprite_width = st.WIDTH * 2
            max_sprite_height = st.HEIGHT * 2

            scaled_width = max(1, min(int(gateway_screen_width), max_sprite_width))
            scaled_height = max(1, min(int(gateway_screen_height), max_sprite_height))
            scaled_gateway = pg.transform.scale(
                gateway_frame,
                (scaled_width, scaled_height),
            )

            draw_start = max(0, int(min(screen_x_a, screen_x_b)))
            draw_end = min(st.WIDTH, int(max(screen_x_a, screen_x_b)) + 1)

            for screen_x in range(draw_start, draw_end):
                wall_depth = self.wall_depths[screen_x]
                if screen_x_b != screen_x_a:
                    t = (screen_x - screen_x_a) / (screen_x_b - screen_x_a)
                    gateway_depth_at_column = 1 / (
                        (1 - t) / camera_depth_a + t / camera_depth_b
                    )
                else:
                    gateway_depth_at_column = average_depth
                if gateway_depth_at_column < wall_depth:
                    source_x = screen_x - int(left)
                    self.screen.blit(
                        scaled_gateway,
                        (screen_x, top),
                        (source_x, 0, 1, scaled_height),
                    )
