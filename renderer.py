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
        #pg.draw.rect(
         #   self.screen, st.FLOOR_COLOR, (0, st.HEIGHT // 2, st.WIDTH, st.HEIGHT // 2)
        #)
        self.render_floor()
        self.render_walls()
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
    
    def get_gateway_ray_intersection(self, ray_dx, ray_dy, render_x, render_y):
        orientation = self.maze.gateway_orientation

        if orientation in ("left", "right"):
            if abs(ray_dx) < 1e-6:
                return None

            distance = (render_x - self.player.x) / ray_dx

        else:
            if abs(ray_dy) < 1e-6:
                return None

            distance = (render_y - self.player.y) / ray_dy

        if distance <= 0:
            return None

        hit_x = self.player.x + distance * ray_dx
        hit_y = self.player.y + distance * ray_dy

        return distance, hit_x, hit_y

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

    def render_floor(self):
        forward_x, forward_y, right_x, right_y = self.get_camera_vectors()

        horizon = st.HEIGHT / 2
        camera_height = 0.5
        focal_length = horizon / mt.tan(st.FOV / 2)

        floor_texture = self.texture_manager.floor_texture
        texture_width = floor_texture.get_width()
        texture_height = floor_texture.get_height()

        # Camera rays through the left and right edges of the screen.
        half_fov_width = mt.tan(st.FOV / 2)

        left_ray_x = forward_x - half_fov_width * right_x
        left_ray_y = forward_y - half_fov_width * right_y

        right_ray_x = forward_x + half_fov_width * right_x
        right_ray_y = forward_y + half_fov_width * right_y

        for screen_y in range(int(horizon) + 1, st.HEIGHT, 4):
            row_depth = (
                camera_height * focal_length
                / (screen_y - horizon)
            )

        for screen_x in range(0, st.WIDTH, 4):
            u = screen_x / (st.WIDTH - 1)

            ray_x = left_ray_x + u * (right_ray_x - left_ray_x)
            ray_y = left_ray_y + u * (right_ray_y - left_ray_y)

            world_x = self.player.x + row_depth * ray_x
            world_y = self.player.y + row_depth * ray_y

            texture_x = int(world_x * 64) % texture_width
            texture_y = int(world_y * 64) % texture_height

            floor_colour = floor_texture.get_at(
                (texture_x, texture_y)
            )

            pg.draw.rect(
                self.screen,
                floor_colour,
                (screen_x, screen_y, 4, 4)
            )

    def render_walls(self):
        self.wall_depths = [float("inf")] * st.WIDTH
        fwd_x, fwd_y, _, _ = self.get_camera_vectors()
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

            # Calculate the visible portion of the original wall.
            visible_top_ratio = (draw_top - top) / projection_height
            visible_bottom_ratio = (draw_bottom - top) / projection_height

            texture_height = texture.get_height()

            texture_top = int(visible_top_ratio * texture_height)
            texture_bottom = int(visible_bottom_ratio * texture_height)

            texture_top = max(0, min(texture_top, texture_height - 1))
            texture_bottom = max(texture_top + 1, min(texture_bottom, texture_height))

            # Crop first, then scale only the visible texture portion.
            visible_column = texture_column.subsurface(
                (0, texture_top, 1, texture_bottom - texture_top)
            )

            scaled_column = pg.transform.scale(
                visible_column,
                (1, draw_bottom - draw_top)
            )

            self.screen.blit(scaled_column, (screen_x, draw_top))

    def render_gateway(self):
        gateway_x, gateway_y = self.maze.gateway_pos
        orientation = self.maze.gateway_orientation

        render_x, render_y = gateway_x, gateway_y

        if orientation == "up":
            render_y = gateway_y + 0.5 - 0.01
        elif orientation == "down":
            render_y = gateway_y - 0.5 + 0.01
        elif orientation == "left":
            render_x = gateway_x + 0.5 - 0.01
        elif orientation == "right":
            render_x = gateway_x - 0.5 + 0.01

        half_width = 0.8 / 2
        frame = self.gateway_animation.get_current_frame()
        texture_width, texture_height = frame.get_size()

        forward_x, forward_y, right_x, right_y = self.get_camera_vectors()
        half_fov = mt.tan(st.FOV / 2)

        for screen_x in range(st.WIDTH):
            u = screen_x / (st.WIDTH - 1)
            camera_x = (2 * u - 1) * half_fov

            ray_dx = forward_x + camera_x * right_x
            ray_dy = forward_y + camera_x * right_y

            intersection = self.get_gateway_ray_intersection(
                ray_dx, ray_dy, render_x, render_y
                )

            if intersection is None:
                continue

            distance, hit_x, hit_y = intersection

        # Check whether the ray hits within the gateway's width.
            if orientation in ("up", "down"):
                offset = hit_x - render_x
            else:
                offset = hit_y - render_y

            if not -half_width <= offset <= half_width:
                continue

        # Camera-space depth corrects perspective projection.
            camera_depth = (
                (hit_x - self.player.x) * forward_x
                + (hit_y - self.player.y) * forward_y
                )

            if camera_depth <= 0.001:
                continue

        # Hide the gateway behind nearer walls.
            if camera_depth >= self.wall_depths[screen_x]:
                continue

            texture_x = int(
                ((offset + half_width) / (2 * half_width)) * texture_width
                )
            texture_x = max(0, min(texture_x, texture_width - 1))

            projected_height = (
                st.GATEWAY_HEIGHT * (st.HEIGHT / 2)
                / (camera_depth * half_fov)
                )

            top = (st.HEIGHT / 2) - projected_height / 2
            bottom = (st.HEIGHT / 2) + projected_height / 2

            draw_top = max(0, int(top))
            draw_bottom = min(st.HEIGHT, int(bottom))

            if draw_bottom <= draw_top:
                continue

        # Map visible screen rows to the corresponding sprite rows.
            top_ratio = (draw_top - top) / projected_height
            bottom_ratio = (draw_bottom - top) / projected_height

            texture_top = max(0, min(
                int(top_ratio * texture_height), texture_height - 1
                ))
            texture_bottom = max(texture_top + 1, min(
                int(bottom_ratio * texture_height), texture_height
                ))

            sprite_column = frame.subsurface(
                (texture_x, texture_top, 1, texture_bottom - texture_top)
                )

            scaled_column = pg.transform.scale(
                sprite_column, (1, draw_bottom - draw_top)
                )

            self.screen.blit(scaled_column, (screen_x, draw_top))